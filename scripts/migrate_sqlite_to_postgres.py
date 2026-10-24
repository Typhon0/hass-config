#!/usr/bin/env python3
"""
High-Performance SQLite to PostgreSQL Data Migration for Home Assistant
Preserves 100% of Home Assistant native schema and copies data with chunking and sequence alignment.
Includes column length adaptations and foreign key handling for seamless migration.
"""

import sys
import time
import sqlite3
import psycopg2
from psycopg2.extras import execute_values

SQLITE_PATH = "file:/root/config/home-assistant_v2.db?mode=ro"
POSTGRES_URL = "postgresql://homeassistant:7*preyKJVcF%26tM1p@192.168.1.170:5432/homeassistant"
CHUNK_SIZE = 20000

def adapt_bytes(val):
    if val is None:
        return None
    if isinstance(val, (bytes, bytearray, memoryview)):
        return psycopg2.Binary(bytes(val))
    return val

def truncate_str(val, max_len):
    if val is None:
        return None
    if isinstance(val, str) and len(val) > max_len:
        return val[:max_len]
    return val

def main():
    print("=" * 60)
    print("🚀 Démarrage de la migration SQLite -> PostgreSQL (Home Assistant)")
    print("=" * 60)

    print("Connexion à SQLite (lecture seule)...")
    sconn = sqlite3.connect(SQLITE_PATH, uri=True)
    scur = sconn.cursor()

    print("Connexion à PostgreSQL...")
    pconn = psycopg2.connect(POSTGRES_URL)
    pconn.set_client_encoding('UTF8')
    pcur = pconn.cursor()

    t_start = time.time()

    # 1. Truncate existing data & drop self-referential FK
    print("\n1. Réinitialisation des tables PostgreSQL...")
    pcur.execute("ALTER TABLE states DROP CONSTRAINT IF EXISTS states_old_state_id_fkey;")
    pconn.commit()

    truncate_query = """
    TRUNCATE TABLE statistics CASCADE;
    TRUNCATE TABLE statistics_short_term CASCADE;
    TRUNCATE TABLE statistics_runs CASCADE;
    TRUNCATE TABLE statistics_meta CASCADE;
    TRUNCATE TABLE states CASCADE;
    TRUNCATE TABLE state_attributes CASCADE;
    TRUNCATE TABLE states_meta CASCADE;
    TRUNCATE TABLE events CASCADE;
    TRUNCATE TABLE event_data CASCADE;
    TRUNCATE TABLE event_types CASCADE;
    TRUNCATE TABLE recorder_runs CASCADE;
    """
    pcur.execute(truncate_query)
    pconn.commit()
    print("✓ Tables réinitialisées.")

    # 2. Migration de event_types
    print("\n2. Migration de event_types...")
    scur.execute("SELECT event_type_id, event_type FROM event_types;")
    rows = [(r[0], truncate_str(r[1], 64)) for r in scur.fetchall()]
    execute_values(pcur, "INSERT INTO event_types (event_type_id, event_type) VALUES %s;", rows)
    pconn.commit()
    print(f"✓ {len(rows)} event_types migrés.")

    # 3. Migration de event_data
    print("\n3. Migration de event_data...")
    scur.execute("SELECT data_id, hash, shared_data FROM event_data;")
    rows = scur.fetchall()
    execute_values(pcur, "INSERT INTO event_data (data_id, hash, shared_data) VALUES %s;", rows)
    pconn.commit()
    print(f"✓ {len(rows)} event_data migrés.")

    # 4. Migration de events
    print("\n4. Migration de events...")
    scur.execute("""
    SELECT event_id, event_type, event_data, origin, origin_idx, time_fired, time_fired_ts,
           context_id, context_user_id, context_parent_id, data_id, context_id_bin,
           context_user_id_bin, context_parent_id_bin, event_type_id
    FROM events;
    """)
    rows = []
    for r in scur.fetchall():
        row = list(r)
        row[11] = adapt_bytes(row[11])
        row[12] = adapt_bytes(row[12])
        row[13] = adapt_bytes(row[13])
        rows.append(tuple(row))
    execute_values(pcur, """
    INSERT INTO events (event_id, event_type, event_data, origin, origin_idx, time_fired, time_fired_ts,
                        context_id, context_user_id, context_parent_id, data_id, context_id_bin,
                        context_user_id_bin, context_parent_id_bin, event_type_id)
    VALUES %s;
    """, rows, page_size=CHUNK_SIZE)
    pconn.commit()
    print(f"✓ {len(rows)} events migrés.")

    # 5. Migration de states_meta
    print("\n5. Migration de states_meta...")
    scur.execute("SELECT metadata_id, entity_id FROM states_meta;")
    rows = [(r[0], truncate_str(r[1], 255)) for r in scur.fetchall()]
    execute_values(pcur, "INSERT INTO states_meta (metadata_id, entity_id) VALUES %s;", rows)
    pconn.commit()
    print(f"✓ {len(rows)} states_meta migrés.")

    # 6. Migration de state_attributes (par batch)
    print("\n6. Migration de state_attributes...")
    scur.execute("SELECT count(*) FROM state_attributes;")
    total_attrs = scur.fetchone()[0]
    print(f"Total à migrer : {total_attrs} attributs...")
    scur.execute("SELECT attributes_id, hash, shared_attrs FROM state_attributes;")
    migrated_attrs = 0
    while True:
        batch = scur.fetchmany(CHUNK_SIZE)
        if not batch:
            break
        execute_values(pcur, "INSERT INTO state_attributes (attributes_id, hash, shared_attrs) VALUES %s;", batch, page_size=CHUNK_SIZE)
        pconn.commit()
        migrated_attrs += len(batch)
        print(f"  -> {migrated_attrs} / {total_attrs} attributs migrés ({migrated_attrs*100/total_attrs:.1f}%)")
    print(f"✓ {migrated_attrs} state_attributes migrés.")

    # 7. Migration de states (par batch)
    print("\n7. Migration de states...")
    scur.execute("SELECT count(*) FROM states;")
    total_states = scur.fetchone()[0]
    print(f"Total à migrer : {total_states} états...")
    scur.execute("""
    SELECT state_id, entity_id, state, attributes, event_id, last_changed, last_changed_ts,
           last_reported_ts, last_updated, last_updated_ts, old_state_id, attributes_id,
           context_id, context_user_id, context_parent_id, origin_idx, context_id_bin,
           context_user_id_bin, context_parent_id_bin, metadata_id
    FROM states;
    """)
    migrated_states = 0
    t_states_start = time.time()
    while True:
        batch = scur.fetchmany(CHUNK_SIZE)
        if not batch:
            break
        adapted_batch = []
        for r in batch:
            row = list(r)
            row[16] = adapt_bytes(row[16])
            row[17] = adapt_bytes(row[17])
            row[18] = adapt_bytes(row[18])
            adapted_batch.append(tuple(row))
        execute_values(pcur, """
        INSERT INTO states (state_id, entity_id, state, attributes, event_id, last_changed, last_changed_ts,
                            last_reported_ts, last_updated, last_updated_ts, old_state_id, attributes_id,
                            context_id, context_user_id, context_parent_id, origin_idx, context_id_bin,
                            context_user_id_bin, context_parent_id_bin, metadata_id)
        VALUES %s;
        """, adapted_batch, page_size=CHUNK_SIZE)
        pconn.commit()
        migrated_states += len(adapted_batch)
        rate = migrated_states / (time.time() - t_states_start)
        print(f"  -> {migrated_states} / {total_states} états ({migrated_states*100/total_states:.1f}%) @ {rate:.0f} rows/s")
    print(f"✓ {migrated_states} states migrés.")

    # Re-add constraint states_old_state_id_fkey
    print("\nRe-création de la contrainte states_old_state_id_fkey...")
    pcur.execute("""
    ALTER TABLE states 
    ADD CONSTRAINT states_old_state_id_fkey 
    FOREIGN KEY (old_state_id) REFERENCES states(state_id) NOT VALID;
    """)
    pconn.commit()
    print("✓ Contrainte réactivée.")

    # 8. Migration de statistics_meta
    print("\n8. Migration de statistics_meta...")
    scur.execute("SELECT id, statistic_id, source, unit_of_measurement, has_mean, has_sum, name, mean_type, unit_class FROM statistics_meta;")
    meta_rows = []
    for r in scur.fetchall():
        row = list(r)
        row[1] = truncate_str(row[1], 255)
        row[2] = truncate_str(row[2], 32)
        row[3] = truncate_str(row[3], 255)
        row[4] = bool(row[4]) if row[4] is not None else None
        row[5] = bool(row[5]) if row[5] is not None else None
        row[6] = truncate_str(row[6], 255)
        row[8] = truncate_str(row[8], 255)
        meta_rows.append(tuple(row))
    execute_values(pcur, """
    INSERT INTO statistics_meta (id, statistic_id, source, unit_of_measurement, has_mean, has_sum, name, mean_type, unit_class)
    VALUES %s;
    """, meta_rows)
    pconn.commit()
    print(f"✓ {len(meta_rows)} statistics_meta migrés.")

    # 9. Migration de statistics_runs
    print("\n9. Migration de statistics_runs...")
    scur.execute("SELECT run_id, start FROM statistics_runs;")
    rows = scur.fetchall()
    execute_values(pcur, "INSERT INTO statistics_runs (run_id, start) VALUES %s;", rows)
    pconn.commit()
    print(f"✓ {len(rows)} statistics_runs migrés.")

    # 10. Migration de statistics (par batch)
    print("\n10. Migration de statistics (Dashboard Énergie & Historique long terme)...")
    scur.execute("SELECT count(*) FROM statistics;")
    total_stats = scur.fetchone()[0]
    print(f"Total à migrer : {total_stats} statistiques...")
    scur.execute("""
    SELECT id, created, created_ts, metadata_id, start, start_ts, mean, mean_weight,
           min, max, last_reset, last_reset_ts, state, sum
    FROM statistics;
    """)
    migrated_stats = 0
    t_stats_start = time.time()
    while True:
        batch = scur.fetchmany(CHUNK_SIZE)
        if not batch:
            break
        execute_values(pcur, """
        INSERT INTO statistics (id, created, created_ts, metadata_id, start, start_ts, mean, mean_weight,
                                min, max, last_reset, last_reset_ts, state, sum)
        VALUES %s;
        """, batch, page_size=CHUNK_SIZE)
        pconn.commit()
        migrated_stats += len(batch)
        rate = migrated_stats / (time.time() - t_stats_start)
        print(f"  -> {migrated_stats} / {total_stats} stats ({migrated_stats*100/total_stats:.1f}%) @ {rate:.0f} rows/s")
    print(f"✓ {migrated_stats} statistics migrés.")

    # 11. Migration de statistics_short_term (par batch)
    print("\n11. Migration de statistics_short_term...")
    scur.execute("SELECT count(*) FROM statistics_short_term;")
    total_short = scur.fetchone()[0]
    print(f"Total à migrer : {total_short} statistiques court terme...")
    scur.execute("""
    SELECT id, created, created_ts, metadata_id, start, start_ts, mean, mean_weight,
           min, max, last_reset, last_reset_ts, state, sum
    FROM statistics_short_term;
    """)
    migrated_short = 0
    t_short_start = time.time()
    while True:
        batch = scur.fetchmany(CHUNK_SIZE)
        if not batch:
            break
        execute_values(pcur, """
        INSERT INTO statistics_short_term (id, created, created_ts, metadata_id, start, start_ts, mean, mean_weight,
                                           min, max, last_reset, last_reset_ts, state, sum)
        VALUES %s;
        """, batch, page_size=CHUNK_SIZE)
        pconn.commit()
        migrated_short += len(batch)
        rate = migrated_short / (time.time() - t_short_start)
        print(f"  -> {migrated_short} / {total_short} stats courtes ({migrated_short*100/total_short:.1f}%) @ {rate:.0f} rows/s")
    print(f"✓ {migrated_short} statistics_short_term migrés.")

    # 12. Alignement des séquences PostgreSQL
    print("\n12. Alignement des séquences d'auto-incrémentation PostgreSQL...")
    seq_queries = [
        ("event_types_event_type_id_seq", "event_types", "event_type_id"),
        ("event_data_data_id_seq", "event_data", "data_id"),
        ("events_event_id_seq", "events", "event_id"),
        ("states_meta_metadata_id_seq", "states_meta", "metadata_id"),
        ("state_attributes_attributes_id_seq", "state_attributes", "attributes_id"),
        ("states_state_id_seq", "states", "state_id"),
        ("statistics_meta_id_seq", "statistics_meta", "id"),
        ("statistics_runs_run_id_seq", "statistics_runs", "run_id"),
        ("statistics_id_seq", "statistics", "id"),
        ("statistics_short_term_id_seq", "statistics_short_term", "id"),
    ]
    for seq, tbl, col in seq_queries:
        query = f"SELECT setval('{seq}', (SELECT COALESCE(MAX({col}), 1) FROM {tbl}));"
        pcur.execute(query)
        val = pcur.fetchone()[0]
        print(f"  -> Séquence {seq} calée à {val}")
    pconn.commit()

    # 13. Optimisation des statistiques du planificateur PostgreSQL
    print("\n13. Exécution de VACUUM ANALYZE sur PostgreSQL...")
    pconn.autocommit = True
    pcur.execute("VACUUM ANALYZE;")
    print("✓ Optimisation terminée.")

    total_time = time.time() - t_start
    print("\n" + "=" * 60)
    print(f"🎉 MIGRATION COMPLÈTE RÉUSSIE EN {total_time:.1f} SECONDES !")
    print("=" * 60)

    sconn.close()
    pconn.close()

if __name__ == "__main__":
    main()
