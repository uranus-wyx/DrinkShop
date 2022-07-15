import React from 'react'
import PropTypes from 'prop-types'
import {Link} from 'react-router-dom'

function ItemDemo({ item:{channel, itemid, name, img} }) {
  return (

    <div className='card shadow-md compact side bg-base-100'>
      <div className="flex-row items-center space-x-4 card-boy">
        <div className='avater'>
          <div className="rounded-full shadow w-14 h-14">
            <img src={img} alt="Profile" />
          </div>
        </div>
        <h2 className="card-title justify-center">
          <Link class="card-title" to={`/item/${itemid}`}>
            {name}
          </Link>
        </h2>  
        <div className="card-actions justify-end">
          <div class="badge badge-secondary">{channel}</div>
        </div>
      </div>
    </div>
  )
}

ItemDemo.prototype = {
  item: PropTypes.object.isRequired
}

export default ItemDemo