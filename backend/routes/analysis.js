import express from 'express'
import axios from 'axios'
import { Router } from 'express'

const ML_SERVICE_API_URL = process.env.ML_SERVICE_API_URL 
const router =Router()
router.route('/analyze').post(async(req,res)=>{
   const {text} =req.body
    if(!text){
        return res.status(400).json({error: 'no text provided'});
    }
    console.log(text);
    try {
        const mlResponse=await axios.post(ML_SERVICE_API_URL,{text})
        const sentimentResult= mlResponse.data.sentiment        
        console.log(sentimentResult);
        res.status(200).json({sentiment:sentimentResult})
    } catch (error) {
        console.log(error);
    }
        })
        export default router