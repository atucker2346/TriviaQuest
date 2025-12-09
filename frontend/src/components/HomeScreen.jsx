import { useEffect, useRef } from 'react'
import './HomeScreen.css'

function HomeScreen({ onStart }) {
  const playerRef = useRef(null)

  useEffect(() => {
    let checkInterval = null
    let initTimeout = null
    let retryCount = 0
    const maxRetries = 50 // 5 seconds max

    const initUnicornStudio = () => {
      // Wait for the element to be in the DOM and visible
      const checkAndInit = () => {
        retryCount++
        if (retryCount > maxRetries) {
          console.error('Unicorn Studio initialization timeout')
          return
        }

        const element = playerRef.current
        if (element && window.UnicornStudio) {
          // Check if element is visible
          const rect = element.getBoundingClientRect()
          if (rect.width === 0 || rect.height === 0) {
            console.log('Element not visible yet, retrying...', rect)
            initTimeout = setTimeout(checkAndInit, 100)
            return
          }

          if (typeof window.UnicornStudio.init === 'function') {
            try {
              console.log('Initializing Unicorn Studio with element:', element)
              console.log('Project ID:', element.getAttribute('data-us-project'))
              window.UnicornStudio.init()
              
              // Check if canvas/iframe was created after a delay
              setTimeout(() => {
                const children = element.children
                console.log('Unicorn Studio children after init:', children.length, children)
                if (children.length === 0) {
                  console.warn('No canvas/iframe created by Unicorn Studio')
                }
              }, 1000)
            } catch (error) {
              console.error('Error initializing Unicorn Studio:', error)
            }
          } else {
            console.warn('UnicornStudio.init is not a function', window.UnicornStudio)
          }
        } else {
          // Retry if element or library not ready
          if (!element) {
            console.log('Element not found, retrying...')
          }
          if (!window.UnicornStudio) {
            console.log('UnicornStudio not loaded, retrying...')
          }
          initTimeout = setTimeout(checkAndInit, 100)
        }
      }
      checkAndInit()
    }

    // Initialize Unicorn Studio script
    if (!window.UnicornStudio) {
      // Check if script is already being loaded
      if (document.querySelector('script[src*="unicornstudio"]')) {
        // Script is loading, wait for it
        checkInterval = setInterval(() => {
          if (window.UnicornStudio) {
            clearInterval(checkInterval)
            setTimeout(() => {
              initUnicornStudio()
            }, 500)
          }
        }, 100)
      } else {
        const script = document.createElement('script')
        script.type = 'text/javascript'
        script.src = 'https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.34/dist/unicornStudio.umd.js'
        script.async = true
        script.onload = () => {
          console.log('Unicorn Studio script loaded', window.UnicornStudio)
          // Wait longer for library to be fully ready
          setTimeout(() => {
            initUnicornStudio()
          }, 500)
        }
        script.onerror = () => {
          console.error('Failed to load UnicornStudio script')
        }
        ;(document.head || document.body).appendChild(script)
      }
    } else {
      // Script already loaded, just initialize
      setTimeout(() => {
        initUnicornStudio()
      }, 500)
    }

    // Cleanup
    return () => {
      if (checkInterval) clearInterval(checkInterval)
      if (initTimeout) clearTimeout(initTimeout)
    }
  }, [])

  return (
    <div className="home-screen">
      <div className="unicorn-studio-container">
        <div 
          ref={playerRef}
          id="unicorn-studio-player"
          data-us-project="ZDTvON5sbZo5DHBfWvHK" 
          className="unicorn-studio-player"
        ></div>
      </div>
      <div className="home-overlay">
        <button className="start-button" onClick={onStart}>
          Start Playing
        </button>
      </div>
    </div>
  )
}

export default HomeScreen
