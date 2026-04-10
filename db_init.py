import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "transit")


async def wait_for_db(retries=5, delay=5):
    """Wait for the database to be ready."""
    for i in range(retries):
        try:
            print(f"Connecting to database (attempt {i + 1}/{retries})...")
            conn = await asyncpg.connect(
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database="postgres",
            )
            await conn.close()
            print("Database connection successful.")
            return True
        except Exception as e:
            print(f"Database not ready: {e}")
            await asyncio.sleep(delay)
    return False


async def init_db():
    try:
        # Wait for the database to be ready
        if not await wait_for_db():
            print("Database not ready after retries. Aborting.")
            return

        # Connect to default postgres DB to create our target DB if it doesn't exist
        conn = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database="postgres",
        )

        # Check if DB exists
        exists = await conn.fetchval(
            f"SELECT 1 FROM pg_database WHERE datname = '{POSTGRES_DB}'"
        )
        if not exists:
            await conn.execute(f"CREATE DATABASE {POSTGRES_DB}")
            print(f"Database '{POSTGRES_DB}' created.")
        await conn.close()

        # Connect to the target DB
        conn = await asyncpg.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
        )

        print("Initializing schema...")

        # Create active_vehicles table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS active_vehicles (
                vehicle_id TEXT PRIMARY KEY,
                route_id TEXT,
                trip_id TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                updated_at TIMESTAMPTZ NOT NULL
            );
        """)

        # Create delay_observations table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS delay_observations (
                observed_at TIMESTAMPTZ NOT NULL,
                stop_id TEXT,
                route_id TEXT,
                trip_id TEXT,
                delay_seconds INTEGER
            );
        """)

        # Create stops table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS stops (
                stop_id TEXT PRIMARY KEY,
                stop_code TEXT,
                stop_name TEXT,
                stop_desc TEXT,
                stop_lat DOUBLE PRECISION,
                stop_lon DOUBLE PRECISION,
                zone_id TEXT,
                stop_url TEXT,
                location_type INTEGER,
                parent_station TEXT,
                wheelchair_boarding INTEGER
            );
        """)

        # Enable pg_trgm extension and create index for fuzzy search
        await conn.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS stops_name_trgm_idx ON stops USING gist (stop_name gist_trgm_ops);
        """)

        # Convert to hypertable
        try:
            await conn.execute(
                "SELECT create_hypertable('delay_observations', 'observed_at', if_not_exists => TRUE);"
            )
            print("Hypertable 'delay_observations' ensured.")
        except Exception as e:
            print(
                f"Note: Could not create hypertable (maybe already exists or TimescaleDB extension missing?): {e}"
            )

        # Create continuous aggregate for hourly delay statistics
        await conn.execute(
            "DROP MATERIALIZED VIEW IF EXISTS hourly_delay_stats CASCADE;"
        )
        await conn.execute("""
            CREATE MATERIALIZED VIEW hourly_delay_stats
            WITH (timescaledb.continuous) AS
            SELECT 
                time_bucket('1 hour', observed_at) AS bucket,
                route_id,
                stop_id,
                avg(delay_seconds) as avg_delay,
                stddev(delay_seconds) as stddev_delay,
                percentile_cont(0.95) WITHIN GROUP (ORDER BY delay_seconds) as p95_delay,
                count(*) as observation_count
            FROM delay_observations
            GROUP BY bucket, route_id, stop_id;
        """)
        print("Continuous aggregate 'hourly_delay_stats' created.")

        await conn.close()
        print("Database initialization complete.")

    except Exception as e:
        print(f"Error during initialization: {e}")


if __name__ == "__main__":
    asyncio.run(init_db())
