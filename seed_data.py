import pandas as pd
from connection import get_db_connection
from dotenv import load_dotenv


db = get_db_connection()
# Cargar .env si lo estás usando
load_dotenv()


# Leer CSV
df = pd.read_csv("CMDB.csv", encoding='utf-8')

# Limpiar encabezados
df.columns = (
    df.columns
    .str.strip()
    .str.replace(r'\s+', '_', regex=True)
    .str.replace(r'[^\w_]', '', regex=True)
    .str.lower()
)

# Verificar columnas clave
print("Columnas detectadas:", df.columns.tolist())
if 'tipo_de_ci' not in df.columns:
    print("❌ Error: columna 'tipo_de_ci' no encontrada.")
    exit()

# Conectar
conn = get_db_connection()
cursor = conn.cursor()

# Insertar o buscar tipo de CI
def get_or_create_citipo(nombre):
    cursor.execute("SELECT id FROM CIType WHERE name = ?", nombre)
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("INSERT INTO CIType (name) VALUES (?)", nombre)
    cursor.execute("SELECT SCOPE_IDENTITY()")
    return cursor.fetchone()[0]

# Parseo de fechas
def parse_date(date_str):
    try:
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except:
        return None

# Insertar registros
for _, row in df.iterrows():
    tipo_id = get_or_create_citipo(row['tipo_de_ci'])

    cursor.execute("""
    INSERT INTO CI (
        Name, Description, SerialNumber, Version, AcquisitionDate,
        CurrentStatus, PhysicalLocation, Owner, SecurityLevel, Compliance,
        ConfigStatus, LicenseNumber, ExpirationDate, TypeId
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    row.get('nombre_del_ci'),
    row.get('descripción'),
    row.get('número_de_serie'),
    row.get('versión'),
    parse_date(row.get('fecha_de_adquisición')),
    row.get('estado_actual'),
    row.get('ubicación_física'),
    row.get('propietarioresponsable'),
    row.get('niveles_de_seguridad'),
    row.get('cumplimiento'),
    row.get('estado_de_configuracin'),
    row.get('nmero_de_licencia'),
    parse_date(row.get('fecha_de_vencimiento')),
    tipo_id
))

print("✅ Datos insertados correctamente.")
cursor.close()
conn.close()
