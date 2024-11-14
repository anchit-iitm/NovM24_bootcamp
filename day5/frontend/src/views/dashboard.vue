<template>
    <div class="dsahboard">
        <h1>dsahboard</h1>
        <button @click="this.testReq()">test</button>
        {{ Response }}
    </div>
</template>

<script>
import axios from 'axios'
    export default{
        data(){
            return{
                Response: "",
                token: null
            }
        },
        beforeCreate(){
            if(localStorage.getItem('authToken') == null){
                this.$router.push({name: 'loginRoute'})
            }
            
        },
        created(){
            this.token = localStorage.getItem('authToken')
        },
        methods:{
            testReq(){
                console.log(this.token);
                
                axios.get('http://localhost:5000/api/storeNew', 
                        {headers: {
                            'Authorization': `${this.token}`
                    }}
                )
                .then((response) => {
                    console.log("good response",response)
                    this.Response = response.data
                })
                .catch((error) => {
                    console.log("bad response",error)
                    this.Response = error.response.data
                })
            }
        }
    }
</script>