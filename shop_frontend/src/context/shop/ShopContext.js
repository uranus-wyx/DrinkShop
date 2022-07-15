import { createContext, useReducer } from "react";
import ShopReducer from "./ShopReducer";

const ShopContext = createContext()

export const ShopProvider = ({children}) => {
  const initialState = {
    items: [],
    item: {},
    loading: false
  }

  const [state, dispatch] = useReducer(ShopReducer, initialState)
  
  return <ShopContext.Provider value={{
    ...state, 
    dispatch
  }}>
    {children}
  </ShopContext.Provider>
}

export default ShopContext