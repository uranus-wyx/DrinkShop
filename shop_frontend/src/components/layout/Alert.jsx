import {useContext} from 'react'
import AlertConext from '../../context/alert/AlertContext'

function Alert() {
  const {alert} = useContext(AlertConext)
  return (
    alert !== null && (
        <p className="flex items-start mb-4 space-x-2">
            {alert.type === 'error' && (
                <svg></svg>
            )}
            <p className="flex-1 text-abse font-semibold leading-7text-white">
                <strong>{alert.msg}</strong>
            </p>
        </p>

    )
  )
}

export default Alert