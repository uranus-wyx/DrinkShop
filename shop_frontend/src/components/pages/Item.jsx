import { FaCodepen, FaStore, FaUserFriends, FaUsers } from 'react-icons/fa'
import { useEffect, useContext } from 'react'
import { useParams } from 'react-router-dom'
import { Link } from 'react-router-dom'
import Spinner from '../layout/Spinner'
import ShopContext from '../../context/shop/ShopContext'
import { getItems } from '../../context/shop/ShopActions'

function Item() {
  
  const {item, loading, dispatch} = useContext(ShopContext)
  const {itemid} = useParams()
  
  useEffect(() => {
    dispatch({type: 'SET_LOADING'})
    const getItemData = async () => {
        const ItemData = await getItems(itemid)
        dispatch({type: 'GET_INFO', payload: ItemData})
    }
    getItemData()
  }, [])

  const {
    channel,
    name,
    price,
    info,
    url,
    img,
  } = item

  if (loading) {
    return <Spinner />
  }
  return (<>
    <div className="w-full image-full mx-auto lg:w-10/12">
      <div className="mb-4">
        <Link to='/' className='btn btn-dark'>
          Back To Search
        </Link>
      </div>
      <div class="card w-96 bg-base-100 shadow-xl">
        <figure class="px-10 pt-10">
            <img src={img} alt="" />
        </figure>
        <div class="card-body items-center text-center">
            <h2 class="card-title">{channel}</h2>
            <p>{info}</p>
            <div class="card-actions">
            <a class="link link-primary" href={url}>More</a>
            </div>
        </div>
      </div>
    </div>  
  </>
  )
}

export default Item