function Loader({ label = "Loading..." }) {
  return (
    <div className="loader-wrap" role="status" aria-live="polite">
      <span className="loader-ring" />
      <p>{label}</p>
    </div>
  );
}

export default Loader;

