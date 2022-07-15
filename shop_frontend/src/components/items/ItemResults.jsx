import {useContext} from 'react'
import Spinner from '../layout/Spinner'
import ItemDemo from './ItemDemo'
import ShopContext from '../../context/shop/ShopContext'

function ItemResults() {

  const {items, loading} = useContext(ShopContext)
  
  if (!loading) {  
    return (
      <div className='grid grid-cols-1 gap-8 xl:grid-cols-4lg:grid-cols-3 md:grid-cols-2'>
        {items.map(item => (
          <ItemDemo key={item.id} item={item}/>
        ))}
      </div>
    )
  } else {
    return <Spinner /> 
  }
  
}

export default ItemResults