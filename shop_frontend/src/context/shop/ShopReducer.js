const ShopReducer = (state, action) => {
  switch (action.type) {
    case 'GET_ITEMS':
      return {
        ...state, 
        items: action.payload,
        loading: false
      }
    case 'GET_INFO':
        return {
          ...state, 
          item: action.payload,
          loading: false
        }

    case 'SET_LOADING':
      return {
        ...state,
        loading:true
      }
    default:
      return state
  }
}

export default ShopReducer