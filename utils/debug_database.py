#!/usr/bin/env python3
"""
Debug script to test database connectivity and insertion
Run this with: python debug_database.py
"""

import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def test_database_connection():
    print("=" * 50)
    print("TESTING DATABASE CONNECTION")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    print(f"✅ Environment variables found:")
    print(f"   DB_NAME: {os.getenv('DB_NAME')}")
    print(f"   DB_USER: {os.getenv('DB_USER')}")
    print(f"   DB_PASSWORD: {'*' * len(os.getenv('DB_PASSWORD', ''))}")
    
    connection_string = (
        f"host=localhost port=5432 "
        f"dbname={os.getenv('DB_NAME')} "
        f"user={os.getenv('DB_USER')} "
        f"password={os.getenv('DB_PASSWORD')}"
    )
    
    try:
        print("\n🔌 Testing database connection...")
        with psycopg.connect(connection_string) as conn:
            with conn.cursor() as cur:
                # Test basic connection
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"✅ Connected to PostgreSQL: {version}")
                
                # Check if table exists
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'nfz_offender'
                    );
                """)
                table_exists = cur.fetchone()[0]
                print(f"✅ Table 'nfz_offender' exists: {table_exists}")
                
                if not table_exists:
                    print("❌ Table doesn't exist! Run your main.py to create it.")
                    return False
                
                # Check table structure
                cur.execute("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'nfz_offender'
                    ORDER BY ordinal_position;
                """)
                columns = cur.fetchall()
                print(f"✅ Table structure:")
                for col in columns:
                    print(f"   {col[0]} ({col[1]}) - Nullable: {col[2]}")
                
                # Check current data
                cur.execute("SELECT COUNT(*) FROM nfz_offender;")
                count = cur.fetchone()[0]
                print(f"✅ Current row count: {count}")
                
                if count > 0:
                    cur.execute("SELECT * FROM nfz_offender LIMIT 3;")
                    rows = cur.fetchall()
                    print("✅ Sample data:")
                    for row in rows:
                        print(f"   {row}")
                
    except psycopg.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def test_insert_sample_data():
    print("\n" + "=" * 50)
    print("TESTING SAMPLE DATA INSERTION")
    print("=" * 50)
    
    connection_string = (
        f"host=localhost port=5432 "
        f"dbname={os.getenv('DB_NAME')} "
        f"user={os.getenv('DB_USER')} "
        f"password={os.getenv('DB_PASSWORD')}"
    )
    
    # Sample drone data (like what would come from your API)
    sample_drone = {
        'id': 'test-drone-12345',
        'x': -500.0,
        'y': 300.0,
        'z': 100.0,
        'first_name': 'Test',
        'last_name': 'User',
        'social_security_number': '123456-789A',
        'phone_number': '+358401234567'
    }
    
    try:
        with psycopg.connect(connection_string) as conn:
            with conn.cursor() as cur:
                print(f"🧪 Inserting test drone: {sample_drone['id']}")
                
                cur.execute('''
                    INSERT INTO nfz_offender (
                        drone_uuid, time, position_x, position_y, position_z,
                        first_name, last_name, social_security, phone_number
                    ) VALUES (
                        %s, NOW(), %s, %s, %s, %s, %s, %s, %s
                    ) ON CONFLICT (drone_uuid) DO UPDATE SET
                        time = NOW(),
                        position_x = EXCLUDED.position_x,
                        position_y = EXCLUDED.position_y,
                        position_z = EXCLUDED.position_z,
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        social_security = EXCLUDED.social_security,
                        phone_number = EXCLUDED.phone_number
                ''', (
                    sample_drone['id'],
                    sample_drone['x'],
                    sample_drone['y'],
                    sample_drone['z'],
                    sample_drone['first_name'],
                    sample_drone['last_name'],
                    sample_drone['social_security_number'],
                    sample_drone['phone_number'],
                ))
                conn.commit()
                print("✅ Test insertion successful!")
                
                # Verify the insertion
                cur.execute("SELECT COUNT(*) FROM nfz_offender WHERE drone_uuid = %s;", (sample_drone['id'],))
                count = cur.fetchone()[0]
                print(f"✅ Verification: Found {count} record(s) with drone_uuid = {sample_drone['id']}")
                
                if count > 0:
                    cur.execute("SELECT * FROM nfz_offender WHERE drone_uuid = %s;", (sample_drone['id'],))
                    row = cur.fetchone()
                    print(f"✅ Inserted data: {row}")
                
    except psycopg.Error as e:
        print(f"❌ Database insertion failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during insertion: {e}")
        return False
    
    return True

def main():
    print("DATABASE DEBUG SCRIPT")
    print("=" * 50)
    
    # Test 1: Database connection
    if not test_database_connection():
        print("\n❌ Database connection test failed. Fix connection issues first.")
        return
    
    # Test 2: Sample data insertion
    if not test_insert_sample_data():
        print("\n❌ Data insertion test failed.")
        return
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("Database connection and insertion are working correctly.")
    print("The issue might be in your application logic or API calls.")
    print("=" * 50)

if __name__ == "__main__":
    main()