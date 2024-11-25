import { Button, MenuItem, Select, selectClasses, Skeleton } from "@mui/material"
import { useQuery } from "@tanstack/react-query"
import { useNavigate, useParams } from "react-router-dom"
import PublicIcon from '@mui/icons-material/Public';
import ApartmentIcon from '@mui/icons-material/Apartment';
import SignpostIcon from '@mui/icons-material/Signpost';
import PersonIcon from '@mui/icons-material/Person';
import Person2Icon from '@mui/icons-material/Person2';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import { useEffect, useState } from "react";
import {toast} from "react-hot-toast"
export type MarketTimeSlots = {
    id: number
    start_time: string
    end_time: string
    cost_multiplier: number
    reserveCount: number
    totalReseve: number
    market: number
    day_of_week: string
}
export type MarketDetail= {
    id: number
    uuid: string
    name: string
    province: number
    city: number
    village: string
    first_manager: string
    second_manager: string
    landline_phone: string
    main_street: string
    rest_address: string
    latitude: string
    longitude: string
    images: Array<string>
    marketTimeSlots: Array<MarketTimeSlots>
  }
export function MarketDetail() {
    const  {id} = useParams()
    const navigate = useNavigate()
    const [timeSlots,setTimeSlots] = useState<{[key:string]:MarketTimeSlots[]}>({})
    const [selectedTime,setSelectedTime]  = useState<number>(0)
    const [weekDay,setWeekDay] = useState<string>("")
    const {data} = useQuery<MarketDetail>({
        queryKey:["Market",id],       
        queryFn:async()=>{
            const res = await fetch(import.meta.env.VITE_BACKEND_URL+"/api/v1/Market/"+id)
            return await res.json()
        }
    },)
    useEffect(()=>{ 
        if(data){
            // data.marketTimeSlots.map((ts)=>{
            //     if (timeSlots[ts.day_of_week]) {
            //         timeSlots[ts.day_of_week].push(ts)
            //     }
            //     else {
            //         timeSlots[ts.day_of_week] = [ts]
            //     }
            // })
            // setTimeSlots({...timeSlots})
            // let weekDay = Object.keys(timeSlots)[0]
            // console.log(timeSlots[weekDay],weekDay)
            // setWeekDay(weekDay)
        }
    },[data])
    const Reserve=async()=>{
        setTimeout(()=>{
        navigate("/success")
        },300)
        const selectedReseve = timeSlots[weekDay][selectedTime!]
        if(selectedReseve.reserveCount<selectedReseve.totalReseve){
           const res = await fetch(import.meta.env.VITE_BACKEND_URL+"api/v1/Market/"+selectedReseve.id+"/",{method:"PATCH"})
           if(res.status==200){
                navigate("/success")
           }else{
               navigate("/success")
               toast.error((await res.json())["data"], { position: "bottom-right" })
           }
        }else{
             toast.error("تایم انتخاب شده پر می باشد")
        }
    }
   return(
    <div className="h-full w-full flex items-center justify-center align-center border-2 gap-5">
        <div className="bg-white/20 max-h-[80%] p-2 rounded-md">
               {data ? (
                   <>
                       <img className="mb-2 max-h-[210px] mx-w-[120px] self-center justify-self-center"
                        //    src={import.meta.env.VITE_BACKEND_URL + data?.images[0]}
                           alt={"مارکت 1"} />

                       <span  className="text-black">مارکت 1</span>
                       <div className="flex flex-col justify-center">
                           <div>
                               <PublicIcon /> <span className="text-black">آذربایجان شرقی</span>
                           </div>
                           <div>
                               <ApartmentIcon /> <span  className="text-black">اسکو</span>
                           </div>
                           <div>
                               <span  className="text-black">اسکو</span>
                           </div>
                           <div>
                               <SignpostIcon /><span  className="text-black">{"test test"}</span>
                           </div>
                           <div>
                               <PersonIcon /><span  className="text-black">{"first manager"}</span>
                           </div>
                           <div>
                               <Person2Icon /><span  className="text-black">{"second manager"}</span>
                           </div>
                           <div className="grid grid-flow-row grid-cols-3 gap-4 my-2">
                               {Object.keys(timeSlots).map((ts, i) => {
                                   console.log(ts,weekDay)
                                   const selected = weekDay===ts?"border-red-600 border-2":""
                                   const isEven  = i % 2 == 0 ? "bg-[#ffb703] rounded-md" : "bg-[#225d5f] rounded-md" 
                                   return (
                                       <div onClick={() => setWeekDay(ts)} key={i} className={selected+ " hover:cursor-pointer p-2 " + isEven}>
                                           {ts}
                                       </div>
                                   )
                               }
                               )}
                           </div>
                           <Select
                               labelId="demo-simple-select-label"
                               id="demo-simple-select"
                               className="mt-5"
                               value={(Object.keys(timeSlots).length!==0)?selectedTime:"0"}
                               onChange={(v)=>setSelectedTime(v.target.value as number)}
                               label="تایم ها قابل رزرو"
                           >                               
                           
                           <MenuItem key={0} value={0}>{"08:00:00"}-{"12:00:00"}<AccessTimeIcon/></MenuItem>
                           </Select>
                           <Button onClick={Reserve} fullWidth variant="contained" className="!my-2"> رزرو</Button>
                       </div>
                   </>
               ) : (
                   <>
                       <Skeleton style={{ width: 210, height: 118 }} variant="rounded"></Skeleton>
                   </>
               )
               }
        </div>

    </div>

   ) 
}