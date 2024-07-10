import React from 'react'
import {createBrowserRouter, RouterProvider} from "react-router-dom" 
import Home from './routes/Home'
import SignUp from './routes/SignUp'
import SignIn from './routes/SignIn'
import "./App.css"
export default function App() {
  const BrowserRouter = createBrowserRouter([
    {path:"/", element:<Home/>},
    {path:"/signup", element:<SignUp/>},
    {path:"/signin", element:<SignIn/>},

    
])
  return (
    <RouterProvider router={BrowserRouter}/>
  )
}
