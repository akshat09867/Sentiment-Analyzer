import express from 'express'
import dotenv from 'dotenv'
import cors from 'cors'
import router from './routes/analysis.js'
const app=express()
dotenv.config(
    {  path:'./.env'}
  )
     app.use(cors())
     app.use(express.json())
     
const port=process.env.Port
app.listen(port,()=>{ console.log(`server is running on port ${port}`)})

app.use('/api/v1',router)