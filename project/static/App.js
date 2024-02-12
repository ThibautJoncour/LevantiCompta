import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [dateHeure, setDateHeure] = useState({});

  useEffect(() => {
    // Appel à l'API Django lors du montage du composant
    axios.get('/api/dateheure/')
      .then(response => {
        setDateHeure(response.data);
      })
      .catch(error => {
        console.error('Erreur lors de la récupération des données:', error);
      });
  }, []); // Le tableau vide indique que cela doit être exécuté une seule fois lors du montage.

  return (
    <div className="App">
      <h1>Levanti Finance</h1>
      <p>Shift your perspective</p>
      <p>Date: {dateHeure.date}</p>
      <p>Heure: {dateHeure.heure}</p>
    </div>
  );
}

export default App;
