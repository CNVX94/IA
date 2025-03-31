import sqlite3
import time

def init_db(db_path='store_data.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            role TEXT,
            content TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS store_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT,
            value TEXT
        )
    ''')
    # Insertar datos iniciales de productos
    sample_products = [
        ('gpu.model.rtx3080', 'NVIDIA GeForce RTX 3080 - 10GB GDDR6X - PCIe 4.0'),
        ('gpu.model.rx6800xt', 'AMD Radeon RX 6800 XT - 16GB GDDR6 - RDNA 2'),
        ('laptop.model.rog_zephyrus', 'ASUS ROG Zephyrus G14 - Ryzen 9 6900HS - RTX 3060 - 16GB DDR5'),
        ('laptop.model.xps15', 'Dell XPS 15 9520 - Core i7-12700H - 32GB RAM - 1TB SSD'),
        ('pc_prebuilt.model.aurora', 'Alienware Aurora R15 - i9-13900KF - RTX 4090 - 64GB DDR5'),
        ('pc_prebuilt.model.legion_t5', 'Lenovo Legion T5 - Ryzen 7 5800 - RTX 3070 Ti - 16GB RAM'),
        ('monitor.model.odyssey_g9', 'Samsung Odyssey G9 - 49" Curvo QLED - 240Hz - 5120x1440'),
        ('monitor.model.predator_x38', 'Acer Predator X38 - 38" Curvo UWQHD+ - 175Hz - G-Sync Ultimate'),
        ('cleaning.air_spray', 'Spray de Aire Comprimido 400ml - Sin CFC - Para electrónicos'),
        ('cleaning.kit_pro', 'Kit de Limpieza: Microfibra + Alcohol Isopropílico + Cepillo Antiestático')
    ]

     # Insertar solo si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM store_info")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT OR IGNORE INTO store_info (key, value)
            VALUES (?, ?)
        ''', sample_products)
        
    conn.commit()
    return conn

def guardar_historial_db(conn, historial):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    cursor = conn.cursor()
    for mensaje in historial:
        rol = "Tú" if mensaje["role"] == "user" else "Bot"
        cursor.execute('''
            INSERT INTO chat_history (timestamp, role, content)
            VALUES (?, ?, ?)
        ''', (timestamp, rol, mensaje['content']))
    conn.commit()

def get_store_info(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM store_info")
    rows = cursor.fetchall()
    # Return information as a dictionary
    return {key: value for key, value in rows}