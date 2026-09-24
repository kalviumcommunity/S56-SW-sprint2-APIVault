const defaultQuestion = 'How do I create a POST endpoint with request body validation?'

function SourcePage({ product, version, question }) {
  const selectedProduct = product || 'FastAPI'
  const selectedVersion = version || 'v0.115.0'
  const selectedQuestion = question || defaultQuestion

  return (
    <main className="answer-source-page">
      <div className="answer-breadcrumb">‹ Answer / Source #1</div>

      <section className="source-summary-card">
        <div className="source-summary-top">
          <div>
            <h1>{selectedProduct} Documentation</h1>
            <div className="source-tags">
              <span className="source-product-tag">{selectedProduct}</span>
              <span className="source-version-tag">{selectedVersion}</span>
            </div>
          </div>

          <a
            className="open-docs-button"
            href="https://fastapi.tiangolo.com/tutorial/first-steps/"
            target="_blank"
            rel="noreferrer"
          >
            Open Docs ↗
          </a>
        </div>

        <div className="source-meta-row">
          <span>Official Documentation</span>
          <span>§ First Steps → Path Operation Decorators</span>
          <span className="source-match">Critical match</span>
        </div>

        <div className="source-url-row">
          https://fastapi.tiangolo.com/tutorial/first-steps/
          <span>Retrieved from indexed source</span>
        </div>
      </section>

      <div className="source-notice">
        <span className="source-notice-icon">ⓘ</span>
        <p>
          The content below is the original documentation excerpt retrieved by APIVault. It is shown in-source and is not AI-generated output.
        </p>
      </div>

      <article className="documentation-excerpt">
        <div className="excerpt-heading">
          <span>Original Documentation — Path Operation Decorators</span>
          <span className="excerpt-badge">CRITICAL DOC</span>
        </div>

        <div className="excerpt-content">
          <h2>Overview</h2>
          <p>
            FastAPI provides automatic request body validation using Python type hints and Pydantic models. The path operation function receives the validated model instance, and FastAPI generates the corresponding OpenAPI schema.
          </p>

          <h2>Declaring a POST route</h2>
          <p>
            To declare a POST endpoint, define the request body with a Pydantic model. FastAPI reads the model schema, validates the incoming JSON, and injects the parsed instance into the path operation function.
          </p>

          <pre className="code-block"><code>{`@app.post("/items/", status_code=201)
async def create_item(item: Item):
    return item`}</code></pre>

          <h2>Validation errors</h2>
          <p>
            If the request body does not match the model schema, FastAPI returns a validation error response with the failing field, its location in the request, and the validation message.
          </p>

          <h2>Response model filtering</h2>
          <p>
            Response models can also validate and filter the response. FastAPI serializes the returned value to match the declared model and excludes fields that are not part of the response schema.
          </p>
        </div>
      </article>

      <div className="answer-source-question">
        <span>Question</span>
        <p>{selectedQuestion}</p>
      </div>

      <a className="back-to-answer" href="#answer">‹ Back to Answer</a>
    </main>
  )
}

export default SourcePage
