function ErrorPage({ product, version, question }) {
  const selectedProduct = product || 'FastAPI'
  const selectedVersion = version || 'v0.115.0'
  const selectedQuestion = question || 'How do I create a POST endpoint with request body validation?'

  const handleRetry = () => {
    window.location.hash = '#ask'
  }

  return (
    <main className="error-page">
      <div className="error-context">
        <span>{selectedProduct}</span>
        <span>{selectedVersion}</span>
      </div>

      <section className="error-card" role="alert">
        <div className="error-icon">!</div>
        <div className="error-content">
          <div className="error-label">REQUEST ERROR</div>
          <h1>Something went wrong</h1>
          <p>
            An unexpected error occurred while processing your request. The documentation service could not complete the search right now.
          </p>

          <div className="error-question">
            <span>Query</span>
            <strong>{selectedQuestion}</strong>
          </div>

          <div className="error-actions">
            <button className="error-retry-button" type="button" onClick={handleRetry}>
              Try Again
            </button>
            <a className="error-report-button" href="mailto:support@apivault.dev?subject=APIVault%20request%20error">
              Report Issue
            </a>
          </div>
        </div>
      </section>
    </main>
  )
}

export default ErrorPage
