import logo from './logo.svg';
import './Main.css';
import DataFetcher from "./DataFetcher";


function Main() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        {/* <DataFetcher /> */}
        <p>
          Edit <code>src/Main.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default Main;