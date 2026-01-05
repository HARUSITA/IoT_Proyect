const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const session = require('express-session');
const path = require('path');

const app = express();
const db = mysql.createConnection({
    host: 'localhost', user: 'root', password: 'mumur05', database: 'sistema_escom'
});

app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(__dirname));
app.use(session({ secret: 'secreto_escom', resave: false, saveUninitialized: true }));

// RUTAS HTML
app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'login.html')));
app.get('/registro', (req, res) => res.sendFile(path.join(__dirname, 'inicio.html')));

app.get('/dashboard', (req, res) => {
    if (!req.session.user) return res.redirect('/');
    if (req.session.rol === 'admin') res.sendFile(path.join(__dirname, 'admin_dashboard.html'));
    else res.sendFile(path.join(__dirname, 'perfil_usuario.html'));
});

// LOGIN
app.post('/login', (req, res) => {
    const { boleta, password } = req.body;
    db.query('SELECT * FROM alumnos WHERE boleta = ? AND password = ?', [boleta, password], (err, results) => {
        if (results.length > 0) {
            req.session.user = results[0];
            req.session.rol = results[0].rol;
            res.redirect('/dashboard');
        } else {
            res.send('<script>alert("Datos incorrectos"); window.location.href="/";</script>');
        }
    });
});

// REGISTRO
app.post('/procesar_registro', (req, res) => {
    const { nombre, boleta, carrera, password, placas, marca_modelo } = req.body;
    db.query('INSERT INTO alumnos (nombre, boleta, carrera, password) VALUES (?, ?, ?, ?)', 
    [nombre, boleta, carrera, password], (err, result) => {
        if (err) return res.send('<script>alert("Boleta ya existe"); window.history.back();</script>');
        
        db.query('INSERT INTO vehiculos (placas, marca_modelo, alumno_id) VALUES (?, ?, ?)', 
        [placas, marca_modelo, result.insertId], (errV) => {
            res.send('<script>alert("Registro Exitoso"); window.location.href="/";</script>');
        });
    });
});

// AGREGAR MOTO
app.post('/agregar_moto', (req, res) => {
    if (!req.session.user) return res.redirect('/');
    db.query('INSERT INTO vehiculos (placas, marca_modelo, alumno_id) VALUES (?, ?, ?)', 
    [req.body.placas, req.body.marca_modelo, req.session.user.id], (err) => {
        if(err) return res.send('<script>alert("Error: Esa placa ya está registrada"); window.history.back();</script>');
        res.redirect('/dashboard');
    });
});

// API ADMIN
app.get('/api/alumnos', (req, res) => {
    if (req.session.rol !== 'admin') return res.status(403).send([]);
    db.query(`SELECT a.id, a.nombre, a.boleta, a.carrera, COUNT(v.id) as num_motos 
              FROM alumnos a LEFT JOIN vehiculos v ON a.id = v.alumno_id 
              WHERE a.rol != 'admin' GROUP BY a.id`, (err, rows) => res.json(rows));
});

app.get('/api/alumno_detalle/:id', (req, res) => {
    const id = req.params.id;
    db.query("SELECT * FROM vehiculos WHERE alumno_id = ?", [id], (e, motos) => {
        db.query(`SELECT * FROM historial WHERE alumno_nombre = (SELECT nombre FROM alumnos WHERE id = ?) ORDER BY id DESC LIMIT 10`, [id], (e, hist) => {
            res.json({ motos, historial: hist });
        });
    });
});

app.get('/api/ultimo_evento', (req, res) => {
    if (req.session.rol !== 'admin') return res.status(403).send({});
    db.query('SELECT * FROM historial ORDER BY id DESC LIMIT 1', (err, result) => {
        res.json(result.length > 0 ? result[0] : null);
    });
});

// --- NUEVA RUTA: OBTENER MIS MOTOS (USUARIO) ---
app.get('/api/mis_motos', (req, res) => {
    if (!req.session.user) return res.status(403).send([]);
    
    // Buscamos solo los vehículos del ID de la sesión actual
    const userId = req.session.user.id;
    db.query('SELECT * FROM vehiculos WHERE alumno_id = ?', [userId], (err, results) => {
        res.json(results);
    });
});

app.listen(3000, () => console.log('🔥 Sistema V5.0 Listo en puerto 3000'));