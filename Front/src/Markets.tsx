import { useQuery } from "@tanstack/react-query"
import { MarketCard } from "./components/MarketCard"
import {TailSpin} from "react-loader-spinner"
import useMediaQuery from "@mui/material/useMediaQuery"
import { useParams, useSearchParams,Link} from "react-router-dom"


export interface IMarket{
  id: number
  uuid: string
  name: string
  village: string
  market_sheba: string
  sheba_owner_name: string
  landline_phone: string
  main_street: string
  rest_address: string
  latitude: string
  longitude: string
  market_type: string
  confirmed_person_national_code: string
  is_confirmed_by_admin: boolean
  created_at: string
  confirmed_date: string
  province: number
  city: number
  first_manager: number
  second_manager: number
}
export  function Market(){
    const matches = useMediaQuery('(min-width:600px)');
    const [searchParams,setSearchParams]  = useSearchParams()
    const {data,isPending} = useQuery({
        queryKey: ["Market",searchParams],
        queryFn:async()=>{
            const res = await fetch(import.meta.env.VITE_BACKEND_URL+"api/v1/Market/?"+searchParams)
            const data:IMarket[] = await res.json()
            return data
        }
    })

    if (isPending){
        return(
            <div className="h-full flex items-center   justify-center ">
                <TailSpin
                    visible={true}
                    height="80"
                    width="80"
                    color="##22c1c3"
                    ariaLabel="tail-spin-loading"
                    radius="1"
                    wrapperStyle={{}}
                    wrapperClass=""
                />
            </div>
            )
    }
    return(
        <>
            {data?.length != 0 ? (
                <div className="grid place-content-center grid-cols-3 gap-64 grid-flow-col p-2">
                    {data?.map((v) =>
                        <>
                            <MarketCard  {...v} />

                        </>)}
                </div>
            ) : <div className="h-full flex-col flex align-center justify-center">
                    <div> متاسفانه در این زمان هیچ مرکزی پیدا نشد </div>
                    <Link className="hover:text-purple-600 text-blue-600" to="/">بازگشت به صفحه جست و جو</Link>
                </div>
            }
        </>
    )

}