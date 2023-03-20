import logo from "./logo.svg";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Chỉnh sửa tập tin <code>src/App.js</code> và lưu để tải lại.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Học React nào!
        </a>
      </header>
    </div>
  );
}

export default App;
