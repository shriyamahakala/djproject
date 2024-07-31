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
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-center">Song Recommendations</h1>


          <form onSubmit={handleSubmit} className="mb-8 space-y-4">
            <div className="flex flex-wrap -mx-2">
              <div className="w-full md:w-1/3 px-2 mb-4 md:mb-0">
                <label className="block text-sm font-medium mb-1">
                  Song:
                  <input type="text" value={inputs.song || ""}  name="song" onChange={handleChange} 
                  className="w-full px-3 py-2 bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"/> 
                </label>
              </div>
                
              <div className="w-full md:w-1/3 px-2 mb-4 md:mb-0">
                <label className="block text-sm font-medium mb-1">
                  Artist:
                  <input type="text" value={inputs.artist || ""} name="artist" onChange={handleChange}
                  className="w-full px-3 py-2 bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"/> 
                </label>
              </div>

              <div className="w-full md:w-1/3 px-2 mb-4 md:mb-0">
                <label className="block text-sm font-medium mb-1">
                Opinion:
                  <input type="text" value={inputs.opinion || ""} name="opinion" onChange={handleChange}
                  className="w-full px-3 py-2 bg-gray-800 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"/> 
                </label>
              </div>
            </div>

            <div className="text-center">
              <button type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900"
              >Submit</button>
            </div>
          </form>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-800">
                  <th className="w-1/3 p-3 font-semibold text-left">Name</th>
                  <th className="w-1/3 p-3 font-semibold text-center">Artist</th>
                  <th className="w-1/3 p-3 font-semibold text-right">BPM</th>
                </tr>
              </thead>
              <tbody>
                {
                  recs.map((obj) => {
                    return (
                      <tr className="border-t border-gray-700">
                        <td className="w-1/3 p-3">{obj.name}</td>
                        <td className="w-1/3 p-3 text-center">{obj.artist}</td>
                        <td className="w-1/3 p-3 text-right">{obj.bpm}</td>
                      </tr>
                    );
                  })
                }
              </tbody>
            </table>
          </div>
      
      </div>
    </div>
  );

}

export default App;
