[Regresar](../README.md)

# Documentación API

## Endpoints principales

- GET /cis - Lista todos los CIs, admite filtros por query params (name, type, status, environment)
- GET /cis/<id> - Obtener CI específico
- POST /cis - Crear nuevo CI
- PUT /cis/<id> - Actualizar CI (requiere campo changed_by)
- GET /cis/<id>/relationships - Obtener relaciones de un CI
- GET /cis/<id>/changes - Historial de cambios (auditoría)

### GET /cis
- Descripción: Obtiene todos los CIs, permite filtros opcionales.
- Query Params:
  - `name` (string) - Filtra por nombre (LIKE %name%)
  - `type` (string) - Filtra por tipo exacto ('servidor', 'base de datos', etc.)
  - `status` (string) - Filtra por estado
  - `environment` (string) - Filtra por ambiente ('DEV', 'QA', 'PROD')
- Respuesta: JSON array con CIs.

### GET /cis/{id}
- Descripción: Obtiene CI específico.
- Respuesta: JSON con los detalles del CI.

### POST /cis
- Descripción: Crea un nuevo CI.
- Body JSON: campos obligatorios `name`, `type`, `environment`, más campos según tipo.
- Respuesta: ID del CI creado.

### PUT /cis/{id}
- Descripción: Actualiza CI.
- Body JSON: campos a modificar + `changed_by`.
- Respuesta: Mensaje de éxito o error.

### GET /cis/{id}/relationships
- Descripción: Obtiene relaciones entrantes y salientes.

### GET /cis/{id}/changes
- Descripción: Obtiene historial de cambios para auditoría.

---

# Ejemplos de algunos endpoint usando Postman

## Mostrar todos los CI
![Busqueda por caracter](./img/mostrarCI.png)

## Obtener relaciones
![Busqueda por caracter](./img/Relaciones.png)

## Registrar logs y Actualizar CI
![Busqueda por caracter](./img/Update.png)

## Registrar logs y Actualizar relacion
![Busqueda por caracter](./img/updaterelacion.png)

## Buscar por caracter
![Busqueda por caracter](./img/busqueda_caracter.png)

[Regresar](../README.md)


# Datos de prueba

```sql

INSERT INTO CI (Name, Description, SerialNumber, Version, AcquisitionDate, CurrentStatus,
    PhysicalLocation, Owner, SecurityLevel, Compliance, ConfigStatus, LicenseNumber,
    ExpirationDate, TypeId, Environment)
VALUES (
    'Servidor2', 'Servidor de archivos compartidos', 'SN234567', 'v2.0', '2021-12-01', 'Activo',
    'Data Center B', 'Equipo de Infraestructura', 'Medio', 'Cumple', 'Aprobado', 'DEF789',
    '2024-12-01', (SELECT Id FROM CIType WHERE Name = 'Hardware'), 'DEV'
);

INSERT INTO CI (Name, Description, Version, AcquisitionDate, CurrentStatus,
    PhysicalLocation, Owner, SecurityLevel, Compliance, ConfigStatus, LicenseNumber,
    ExpirationDate, TypeId, Environment)
VALUES (
    'Base de Datos1', 'Base de datos de clientes', 'v12.3', '2020-10-15', 'Activo',
    'Rack DB1', 'Equipo DBA', 'Alto', 'Cumple', 'Aprobado', 'GHI012',
    '2025-03-30', (SELECT Id FROM CIType WHERE Name = 'Base de Datos'), 'QA'
);

INSERT INTO CI (Name, Description, Version, AcquisitionDate, CurrentStatus,
    PhysicalLocation, Owner, SecurityLevel, Compliance, ConfigStatus, LicenseNumber,
    ExpirationDate, TypeId, Environment)
VALUES (
    'Aplicación Web', 'Sistema de gestión de usuarios', 'v1.2.3', '2022-09-20', 'Activo',
    'Servidor2', 'Equipo de Desarrollo', 'Medio', 'Cumple', 'Aprobado', 'JKL345',
    '2025-06-01', (SELECT Id FROM CIType WHERE Name = 'Software'), 'PROD'
);

INSERT INTO CI (Name, Description, SerialNumber, Version, AcquisitionDate, CurrentStatus,
    PhysicalLocation, Owner, SecurityLevel, Compliance, ConfigStatus, LicenseNumber,
    ExpirationDate, TypeId, Environment)
VALUES (
    'Switch-Core', 'Switch principal de red LAN', 'SN889900', 'v3.0', '2019-08-10', 'Activo',
    'Rack Red Principal', 'Redes y Comunicaciones', 'Crítico', 'Cumple', 'Aprobado', 'MNO678',
    '2026-08-01', (SELECT Id FROM CIType WHERE Name = 'Red'), 'DEV'
);

INSERT INTO CI (Name, Description, SerialNumber, Version, AcquisitionDate, CurrentStatus,
    PhysicalLocation, Owner, SecurityLevel, Compliance, ConfigStatus, LicenseNumber,
    ExpirationDate, TypeId, Environment)
VALUES (
    'Firewall', 'Firewall de perímetro', 'SN445566', 'v4.5', '2020-05-05', 'Activo',
    'Rack Seguridad', 'Equipo Seguridad TI', 'Crítico', 'Cumple', 'Aprobado', 'PQR901',
    '2025-05-01', (SELECT Id FROM CIType WHERE Name = 'Seguridad'), 'QA'
);

INSERT INTO CI (Name, Description, SerialNumber, Version, AcquisitionDate, CurrentStatus,
    PhysicalLocation, Owner, SecurityLevel, Compliance, ConfigStatus, LicenseNumber,
    ExpirationDate, TypeId, Environment)
VALUES (
    'Servidor DevOps', 'Servidor para integración continua', 'SN998877', 'v1.4', '2021-07-01', 'Activo',
    'Rack DevOps', 'Equipo DevOps', 'Alto', 'Cumple', 'Aprobado', 'STU234',
    '2024-09-01', (SELECT Id FROM CIType WHERE Name = 'Hardware'), 'DEV'
);

INSERT INTO CI (Name, Description, Version, AcquisitionDate, CurrentStatus,
    PhysicalLocation, Owner, SecurityLevel, Compliance, ConfigStatus, LicenseNumber,
    ExpirationDate, TypeId, Environment)
VALUES (
    'Repositorio Código', 'Repositorio central de código fuente', 'v3.1', '2022-11-01', 'Activo',
    'Cloud Git Repo', 'Equipo Desarrollo', 'Medio', 'Cumple', 'Aprobado', 'VWX567',
    '2025-11-01', (SELECT Id FROM CIType WHERE Name = 'Software'), 'PROD'
);
```