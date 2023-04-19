import "./App.css";
import {Title} from "./components/Title";
import {Searchbar} from "./components/Searchbar";
import {Graph} from "./components/Graph";

function App() {
  return (
    <div className="App">
      <p>UIUC Scraper</p>

      <Title/>
      <Searchbar></Searchbar>
      <Graph></Graph>
      
    </div>
  );
}

export default App;
