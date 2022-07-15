import React from 'react'
import {useState, useContext} from 'react'
import ShopContext from '../../context/shop/ShopContext'
import { searchItems } from '../../context/shop/ShopActions'
import AlertContext from '../../context/alert/AlertContext'

function ItemSearch() {

  const [text, setText] = useState('')
  const {dispatch} = useContext(ShopContext)
  const {setAlert} = useContext(AlertContext)

  const handleChange = (e) => setText(e.target.value)
  const handleSubmit = async (e) => {
    e.preventDefault()

    if (text === '') {
        setAlert('please enter sth', 'error')
    } else {
      
      dispatch({type:'SET_LOADING'})
      const items = await searchItems(text)
      dispatch({type:'GET_ITEMS', payload: items})

      setText('')
    }
  }

  return (
    <div className='grid grid-cols-1 xl:grid-cols-2 lg:grid-cols-2 md:grid-cols-2 mb-8 gap-8'>
      <div>
        <form onSubmit={handleSubmit}>
          <div className="form-control">
            <div className="relative">
              <input 
                type="text" 
                className="w-full pr-40 bg-gray-200 input input-lg text-black" 
                placeholder='Search'
                value={text}
                onChange={handleChange}
              />
              <button 
                type='submit'
                className="absolute top-0 right-0 rounded-l-none w-36 btn btn-lg"
              >
                Go
              </button>
            </div>
          </div>
        </form>
      </div>
      {/* {items.length > 0 && (
        <div>
          <button
          onClick={() => dispatch({type:'CLEAR_ITEMS'})} 
            className="btn btn-ghost btn-lg"
          >Clear</button>
        </div> 
      )} */}
       
    </div>
  )
}

export default ItemSearch