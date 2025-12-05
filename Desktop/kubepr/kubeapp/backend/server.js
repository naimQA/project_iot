import express from 'express';
import mysql from 'mysql2/promise';
import cors from 'cors';

const app = express();
app.use(express.json());
app.use(cors());

const db = await mysql.createPool({
  host: process.env.DB_HOST ,
  user: process.env.DB_USER ,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME ,
   authPlugins: {
    mysql_native_password: () => require('mysql2/lib/auth_plugins').caching_sha2_password
  }
});

app.get('/etudiants', async (req, res) => {
  const [rows] = await db.query('SELECT * FROM etudiants');
  res.json(rows);
});

app.post('/etudiants', async (req, res) => {
  const { nom, prenom, email, age } = req.body;
  await db.query('INSERT INTO etudiants(nom, prenom, email, age) VALUES (?, ?, ?, ?)',
    [nom, prenom, email, age]);
  res.json({ message: 'Ajouté' });
});

app.put('/etudiants/:id', async (req, res) => {
  const { nom, prenom, email, age } = req.body;
  const { id } = req.params;
  await db.query("UPDATE etudiants SET nom=?, prenom=?, email=?, age=? WHERE id=?",
    [nom, prenom, email, age, id]);
  res.json({ message: 'Modifié' });
});

app.delete('/etudiants/:id', async (req, res) => {
  await db.query("DELETE FROM etudiants WHERE id=?", [req.params.id]);
  res.json({ message: 'Supprimé' });
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log('API running on ' + port));
