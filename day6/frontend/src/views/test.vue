<template>
    <div class="test">
        <h1>hello world</h1>
        <p>{{ frontend_message }}</p>
        <p>{{ frontend_args }}</p>
        <input type="number" name="" id="" placeholder="add the int" v-model="this.variableInt"><br>
        <button @click="testput(this.variableInt)">Test Connection</button>
        <button @click="testput1()">Test Connection</button>
    </div>    
</template>

<script>
    import axios from 'axios'
    export default{
        name: 'testPage',
        data(){
            return{
                frontend_message: null,
                frontend_args: null,
                variableInt: null
            }
        },
        created(){
            console.log("beforeCreate")
            this.testConnection()
        },
        methods:{
            async testConnection(){
                    axios
                        .get('http://localhost:5000/api/')
                        .then((response) => {
                            console.log("good response",response)
                            this.frontend_message = response.data.message
                        })
                        .catch((error) => {
                            console.log("bad response",error)
                        })
            },
            async testput(id){
                    axios
                        .put(`http://localhost:5000/api/${id}`)
                        .then((response) => {
                            console.log("good response",response)
                            this.frontend_message = response.data.message
                            this.frontend_args = response.data.variable_passed
                        })
                        .catch((error) => {
                            console.log("bad response",error)
                        })
            },
            async testput1(){
                    axios
                        .put(`http://localhost:5000/api/${this.variableInt}`)
                        .then((response) => {
                            console.log("good response",response)
                            this.frontend_message = response.data.message
                            this.frontend_args = response.data.variable_passed
                        })
                        .catch((error) => {
                            console.log("bad response",error)
                        })
            }
        }
    }
</script>

<style></style>