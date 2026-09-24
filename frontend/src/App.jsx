import { useEffect, useState } from 'react'
import Header from './components/Header'
import ProductSelector from './components/ProductSelector'
import VersionSelector from './components/VersionSelector'
import QuestionInput from './components/QuestionInput'
import ExampleQuestions from './components/ExampleQuestions'
import Sidebar from './components/Sidebar'
import HistoryPage from './components/HistoryPage'
import DocumentationPage from './components/DocumentationPage'
import AnswerSourcePage from './components/AnswerSourcePage'
import SourcePage from './components/SourcePage'
import ErrorPage from './components/ErrorPage'
import StateNavigator from './components/StateNavigator'
import './App.css'

function App() {
  const getPageFromHash = () => {
    if (window.location.hash === '#history') {
      return 'history'
    }

    if (window.location.hash === '#documentation') {
      return 'documentation'
    }

    if (window.location.hash === '#answer') {
      return 'answer'
    }

    if (window.location.hash === '#source') {
      return 'source'
    }

    if (window.location.hash === '#error') {
      return 'error'
    }

    return 'ask'
  }

  const [page, setPage] = useState(getPageFromHash())
  const [product, setProduct] = useState('')
  const [version, setVersion] = useState('')
  const [question, setQuestion] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const handleHashChange = () => {
      setPage(getPageFromHash())
    }

    window.addEventListener('hashchange', handleHashChange)

    return () => {
      window.removeEventListener('hashchange', handleHashChange)
    }
  }, [])

  const handleAskQuestion = () => {
    if (!product || !version || !question.trim()) {
      setError('Select a product, version, and enter a question.')
      return
    }

    setError('')
    setLoading(true)

    console.log({
      product,
      version,
      question,
    })

    setTimeout(() => {
      setLoading(false)
      window.location.hash = '#answer'
    }, 1000)
  }

  const handleProductChange = (selectedProduct) => {
    setProduct(selectedProduct)
    setVersion('')
    setError('')
  }

  const handleExampleSelect = (
    selectedQuestion,
    selectedProduct,
    selectedVersion
  ) => {
    setQuestion(selectedQuestion)
    setProduct(selectedProduct)
    setVersion(selectedVersion)
    setError('')
  }

  return (
    <div className="app-shell">
      <Header activePage={page} />

      {page === 'history' ? (
        <HistoryPage />
      ) : page === 'documentation' ? (
        <DocumentationPage />
      ) : page === 'answer' ? (
        <AnswerSourcePage
          product={product}
          version={version}
          question={question}
        />
      ) : page === 'source' ? (
        <SourcePage
          product={product}
          version={version}
          question={question}
        />
      ) : page === 'error' ? (
        <ErrorPage
          product={product}
          version={version}
          question={question}
        />
      ) : (
        <div className="page-layout">
          <main className="main-content">
            <div className="hero">
              <div className="badge-row">
                <span>
                  <span className="dot" /> Version-aware
                </span>
                <span>Source-grounded</span>
                <span>Developer-first</span>
              </div>

              <h1>
                Version-Aware Technical
                <br />
                Documentation Assistant
              </h1>

              <p>
                Select a product and version. Ask a technical question. Get a
                grounded answer with the exact documentation source — every time.
              </p>
            </div>

            <section className="question-card">
              <div className="selectors">
                <ProductSelector
                  product={product}
                  onProductChange={handleProductChange}
                />

                <VersionSelector
                  product={product}
                  version={version}
                  onVersionChange={setVersion}
                />
              </div>

              <QuestionInput
                question={question}
                onQuestionChange={setQuestion}
              />

              <div className="submit-row">
                <button
                  className="ask-button"
                  onClick={handleAskQuestion}
                  disabled={loading}
                >
                  {loading ? 'Asking...' : '⌕ Ask Question'}
                </button>
              </div>

              {error && (
                <div className="form-error">
                  {error}
                </div>
              )}
            </section>

            <ExampleQuestions onSelect={handleExampleSelect} />
          </main>

          <Sidebar />
        </div>
      )}

      <StateNavigator
        activeState={
          page === 'answer'
            ? 'Answer'
            : page === 'source'
              ? 'Source'
              : page === 'error'
                ? 'Error'
                : page === 'ask'
                ? 'Ask'
                : 'demo'
        }
      />
    </div>
  )
}

export default App