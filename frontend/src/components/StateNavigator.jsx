function StateNavigator({ activeState = 'demo' }) {
  const states = [
    { label: 'demo', href: '#ask' },
    { label: 'Ask', href: '#ask' },
    { label: 'Loading' },
    { label: 'Answer', href: '#answer' },
    { label: 'Source', href: '#source' },
    { label: 'No Docs' },
    { label: 'Error', href: '#error' },
  ]

  return (
    <nav className="state-navigator" aria-label="Demo states">
      {states.map((state) => {
        const className = activeState.toLowerCase() === state.label.toLowerCase()
          ? 'state-item active'
          : 'state-item'

        if (!state.href) {
          return (
            <span className={className} key={state.label}>
              {state.label}
            </span>
          )
        }

        return (
          <a className={className} href={state.href} key={state.label}>
            {state.label}
          </a>
        )
      })}
    </nav>
  )
}

export default StateNavigator
