import { useState,useEffect } from "react"
import Button from '@mui/material/Button';
import { faIR } from '@mui/x-date-pickers/locales';
import {FormControl, InputLabel, MenuItem, Select, SelectChangeEvent, Skeleton} from '@mui/material';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import { useQuery } from "@tanstack/react-query";
import { MobileDatePicker, LocalizationProvider,MobileTimePicker } from "@mui/x-date-pickers";
import { AdapterMomentJalaali } from '@mui/x-date-pickers/AdapterMomentJalaali';
import { IMarket } from "./Markets";
import "./Home.css"
import { useNavigate, createSearchParams } from "react-router-dom";


interface ICity{
    id:number,
    name: string
}
interface IProvicne{
    id:number
    name:string
    cities:ICity[]
}
interface IInputparams {
    prov?:string,
    city?:string,
    byDate:boolean,
    byName:boolean,
    name?:string,
    date?:string,
    time?:string,
}
const weekDays = [
    'شنبه',
    'یکشنبه',
    'دوشنبه',
    'سه‌شنبه',
    'چهارشنبه',
    'پنج‌شنبه',
    'جمعه'
]
export function Home() {
    const [inputParams,setInput] = useState<IInputparams>({byDate:false,byName:true,date:"شنبه"})
    const [MarketIdx,setMarketIdx] = useState(1)
    const [province,setProvince] = useState<IProvicne[]>([])
    const [provIdx,setProvIdx] = useState(0)
    const [cityName,setCityName] = useState("اسکو")
    const {data:Markets,isPending} = useQuery({
        queryKey: ["Market"+cityName],
        queryFn:async()=>{
            const res = await fetch(import.meta.env.VITE_BACKEND_URL+"/api/v1/Market/City/"+cityName)
            const data:IMarket[] = await res.json()
            return data
        }
    })
    const {data} = useQuery({
        queryKey: ["Provinces"],
        queryFn:async()=>{
            const res = await fetch(import.meta.env.VITE_BACKEND_URL+"/api/v1/Province/")
            const data:IProvicne[] = await res.json()
            return data
        }
    })
    const navigate = useNavigate()
    useEffect(() => {
        if (data) {
            setProvince(data)
        }
    }, [data])
    const search =()=>{
        if(inputParams.byName){
            navigate("/market-detail/" + MarketIdx) 
        }else{
            navigate({pathname:"market/",search: createSearchParams({ date: inputParams.date!, time: inputParams.time!}).toString() })
        }
    }
    return(
        <div className="flex justify-center align-middle items-center flex-col h-full">
            <div dir="rtl" className="card  flex flex-col p-5 space-y-4 rounded-md">
                <InputLabel id="demo-simple-select-label">استان</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={province.length != 0 ? "" + province[provIdx].id : ""}
                    label="استان"
                    onChange={(e: SelectChangeEvent) => {
                        let provIdx =  parseInt(e.target.value)-1
                        setProvIdx(provIdx)
                        setCityName(province[provIdx].cities[0].name)
                        }
                    }
                >
                    {province.length!=0 && province.map((v, i) => (
                        <MenuItem key={i} value={v.id}>{v.name}</MenuItem>
                    ))}
                </Select>
                <InputLabel id="demo-simple-select-label">شهر</InputLabel>
                {province.length!=0?
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    label="شهر"
                    value={cityName}
                        onChange={(e: SelectChangeEvent) => {
                            setCityName(e.target.value)
                        }}
                >
                    {province.length!=0 && province[provIdx].cities.map((v, i) => (
                        <MenuItem key={i} value={v.name}>{v.name}</MenuItem>
                    ))}
                </Select>:<Skeleton style={{width:190,height:22}} variant="rounded"></Skeleton>
                }
                <FormControl className="items-center">
                    <RadioGroup
                        row
                        aria-labelledby="demo-radio-buttons-group-label"
                        defaultValue="date"
                        name="radio-buttons-group"
                    >
                        <FormControlLabel control={<Radio />} checked={inputParams.byDate}
                            value="date"
                            dir="rtl"
                            onChange={() => setInput({ ...inputParams, byName: !inputParams.byName, byDate: !inputParams.byDate })}
                            label="بر اساس تاریخ" />
                        <FormControlLabel control={<Radio />}
                            value="name"
                            checked={inputParams.byName} 
                            onChange={() => setInput({ ...inputParams, byName: !inputParams.byName, byDate: !inputParams.byDate })}
                            dir="rtl"
                            label="بر اساس نام " />
                    </RadioGroup>
                </FormControl>
                <div className={inputParams.byDate ? "display flex flex-col m-2" : "hide"}>
                    <LocalizationProvider localeText={faIR.components.MuiLocalizationProvider.defaultProps.localeText}  dateAdapter={AdapterMomentJalaali}>
                        <Select id="demo-simple-select" label="روز" value={inputParams.date}
                            onChange={(e: SelectChangeEvent) => {
                                setInput({ ...inputParams, date: e.target.value })
                            }}
                        >{weekDays.map((v, i) => (
                            <MenuItem key={i} value={v}>{v}</MenuItem>
                        ))}

                        </Select>
                            
                        <MobileTimePicker label="ساعت" onChange={(e) => {
                            setInput({ ...inputParams, time: e?.toDate().toUTCString() })
                        }} />
                    </LocalizationProvider>
                </div>
                <div className={inputParams.byName ? "display" : "hide"}>
                    {Markets? (<Select  className="max-w-prose" fullWidth disabled={isPending||Markets.length==0}
                        onChange={(v) => {
                                setMarketIdx(parseInt(v.target.value))
                        }
                        }
                     value={MarketIdx+""} label="نام مرکز:" variant="outlined" >
                        {
                            Markets.map((market,idx) =>
                                <MenuItem key={idx}  value={market.id}>{market.name}</MenuItem>
                            )
                        }
                    </Select>)
                        :
                        <></>}
                </div>
            <Button onClick={search} variant="contained" className="bg-blue-500 rounded-md p-2 text-center">جست و جو </Button>
            </div>
        </div>
    )
    
}