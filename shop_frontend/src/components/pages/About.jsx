import React from 'react'
import { useEffect, useContext } from 'react'

function About() {
  useEffect(()=>{
        console.log('i fire once');
  },[]);
  return (
    <div>
      <h1 className="text-6xl mb-4">Shop</h1>
    </div>
  )
}

export default About