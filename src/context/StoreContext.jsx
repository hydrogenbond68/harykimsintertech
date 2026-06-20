// src/context/StoreContext.jsx
import { createContext, useContext, useReducer, useEffect, useCallback } from 'react';
import { productService, categoryService, orderService, wishlistService, reviewService } from '../services/shopService';
import { useAuth } from './AuthContext';
import { toast } from 'react-toastify';

const StoreContext = createContext();

const initialState = {
  products: [],
  categories: [],
  brands: [],
  cart: [],
  wishlist: [],
  orders: [],
  reviews: [],
  loading: false,
  isInitialized: false,
};

function appReducer(state, action) {
  switch (action.type) {
    case 'SET_INITIALIZED':
      return { ...state, isInitialized: true };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_PRODUCTS':
      return { ...state, products: action.payload };
    case 'SET_CATEGORIES':
      return { ...state, categories: action.payload };
    case 'SET_BRANDS':
      return { ...state, brands: action.payload };
    case 'SET_CART':
      return { ...state, cart: action.payload };
    case 'SET_WISHLIST':
      return { ...state, wishlist: action.payload };
    case 'SET_ORDERS':
      return { ...state, orders: action.payload };
    case 'SET_REVIEWS':
      return { ...state, reviews: action.payload };
    case 'ADD_TO_CART': {
      const existingItem = state.cart.find(item => item.id === action.payload.id);
      if (existingItem) {
        return {
          ...state,
          cart: state.cart.map(item =>
            item.id === action.payload.id
              ? { ...item, quantity: item.quantity + (action.payload.quantity || 1) }
              : item
          ),
        };
      }
      return {
        ...state,
        cart: [...state.cart, { ...action.payload, quantity: action.payload.quantity || 1 }],
      };
    }
    case 'REMOVE_FROM_CART':
      return {
        ...state,
        cart: state.cart.filter(item => item.id !== action.payload),
      };
    case 'UPDATE_CART_QUANTITY':
      return {
        ...state,
        cart: state.cart.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: action.payload.quantity }
            : item
        ),
      };
    case 'CLEAR_CART':
      return { ...state, cart: [] };
    default:
      return state;
  }
}

export function StoreProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);
  const { user } = useAuth();

  const fetchInitialData = useCallback(async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const [products, categories, brands] = await Promise.all([
        productService.getProducts(),
        categoryService.getCategories(),
        categoryService.getBrands()
      ]);
      dispatch({ type: 'SET_PRODUCTS', payload: products });
      dispatch({ type: 'SET_CATEGORIES', payload: categories });
      dispatch({ type: 'SET_BRANDS', payload: brands });

      if (user) {
        const [orders, wishlist] = await Promise.all([
          orderService.getMyOrders(),
          wishlistService.getWishlist()
        ]);
        dispatch({ type: 'SET_ORDERS', payload: orders });
        dispatch({ type: 'SET_WISHLIST', payload: wishlist });
      }
    } catch (error) {
      console.error('Failed to fetch initial data:', error);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
      dispatch({ type: 'SET_INITIALIZED' });
    }
  }, [user]);

  useEffect(() => {
    fetchInitialData();
  }, [fetchInitialData]);

  // Sync cart with localStorage
  useEffect(() => {
    const storedCart = localStorage.getItem('cart');
    if (storedCart) {
      try {
        dispatch({ type: 'SET_CART', payload: JSON.parse(storedCart) });
      } catch (e) {
        localStorage.removeItem('cart');
      }
    }
  }, []);

  useEffect(() => {
    if (state.isInitialized) {
      localStorage.setItem('cart', JSON.stringify(state.cart));
    }
  }, [state.cart, state.isInitialized]);

  const addToCart = (product, quantity = 1) => {
    if (product.stock_quantity < quantity) {
      toast.error('Not enough stock available');
      return;
    }
    dispatch({ type: 'ADD_TO_CART', payload: { ...product, quantity } });
    toast.success('Added to cart!');
  };

  const removeFromCart = (productId) => {
    dispatch({ type: 'REMOVE_FROM_CART', payload: productId });
    toast.info('Removed from cart');
  };

  const updateQuantity = (productId, quantity) => {
    const product = state.products.find(p => p.id === productId);
    if (product && quantity > product.stock_quantity) {
      toast.error(`Only ${product.stock_quantity} units available`);
      return;
    }
    dispatch({ type: 'UPDATE_CART_QUANTITY', payload: { id: productId, quantity } });
  };

  const toggleWishlist = async (product) => {
    if (!user) {
      toast.warning('Please login to manage wishlist');
      return;
    }
    try {
      const exists = state.wishlist.find(item => item.product_id === product.id);
      if (exists) {
        await wishlistService.removeFromWishlist(product.id);
        dispatch({
          type: 'SET_WISHLIST',
          payload: state.wishlist.filter(item => item.product_id !== product.id)
        });
        toast.info('Removed from wishlist');
      } else {
        const newItem = await wishlistService.addToWishlist(product.id);
        dispatch({ type: 'SET_WISHLIST', payload: [...state.wishlist, newItem] });
        toast.success('Added to wishlist');
      }
    } catch (error) {
      toast.error('Failed to update wishlist');
    }
  };

  const placeOrder = async (orderData) => {
    if (!user) {
      toast.error('Please login to place an order');
      return;
    }
    try {
      const items = state.cart.map(item => ({
        product_id: item.id,
        quantity: item.quantity,
        price: item.price
      }));

      const newOrder = await orderService.createOrder({
        ...orderData,
        items
      });

      dispatch({ type: 'CLEAR_CART' });
      dispatch({ type: 'SET_ORDERS', payload: [newOrder, ...state.orders] });
      toast.success('Order placed successfully!');
      return newOrder.id;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to place order');
      throw error;
    }
  };

  return (
    <StoreContext.Provider value={{
      ...state,
      addToCart,
      removeFromCart,
      updateQuantity,
      toggleWishlist,
      placeOrder,
      refreshData: fetchInitialData
    }}>
      {children}
    </StoreContext.Provider>
  );
}

export function useStore() {
  const context = useContext(StoreContext);
  if (!context) {
    throw new Error('useStore must be used within StoreProvider');
  }
  return context;
}
