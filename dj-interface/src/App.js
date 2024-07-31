import React, {useState, useEffect} from 'react';
import './App.css';

function App() {


  const [learned, setLearned] = useState(0);
  const [inputs, setInputs] = useState({});

  const [recs, setRecs] = useState([]);

  const handleSubmit = (event) => {
    // getData(inputs);
    getData(inputs);
    setInputs({
      song: "",
      artist: "",
      opinion: ""
    });
    event.preventDefault();
    
    // alert(`The name you entered was: ${song}`)
  }

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs(values => ({...values, [name]: value}))
  }


  function getData(formData) {
    
    const song = formData["song"];
    const artist = formData["artist"];
    const opinion = formData["opinion"];

    
    fetch('/songRated', {
      method: "POST",
      headers: {
      'Content-Type' : 'application/json'
      },
      body: JSON.stringify({"learned": learned, "currSong": song, "currArtist": artist, "opinion": opinion})
      }).then(res => res.json()).then(data => {
        console.log(data);
        setLearned(learned+1)
        setRecs(data);
    });

  } 
  
  
  return (
    <div className="App">
      <header className="App-header">
      <form onSubmit={handleSubmit}>
        <label>
          Song:
          <input type="text" value={inputs.song || ""}  name="song" onChange={handleChange}/> 
        </label>
        <label>
          Artist:
          <input type="text" value={inputs.artist || ""} name="artist" onChange={handleChange}/> 
        </label>
        <label>
          Opinion:
          <input type="text" value={inputs.opinion || ""} name="opinion" onChange={handleChange}/> 
        </label>
        <button type="submit">Submit</button>
      </form>
      <table style={{width: '100%'}}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Artist</th>
            <th>BPM</th>
          </tr>
        </thead>
        <tbody>
          {
            recs.map((obj) => {
              return (
                <tr>
                  <td>{obj.name}</td>
                  <td>{obj.artist}</td>
                  <td>{obj.bpm}</td>
                </tr>
              );
            })
          }
        </tbody>
      </table>
      </header>
    </div>
  );

}

export default App;
