<template>
    <div class="login_page">
        <h2>Login page</h2>
        <form>
            <label for="emailid">email: </label>
            <input type="email" name="emailid" id="" placeholder="add the email" v-model="this.frontend_email"><br><br>
            <label for="passwrrd">passwrrd: </label>
            <input type="password" name="passwrrd" id="write the password" v-model="this.frontend_password"><br><br>
            <button type="button" @click="this.loginRequest()">Login</button>
        </form>
        {{ this.frontend_message }}
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: "login",
    data() {
        return {
            frontend_message: "",
            frontend_email: "",
            frontend_password: "",
        };
    },
    methods:{
        test(){
            console.log("email", this.frontend_email)
            console.log("passwrod", this.frontend_password)
        },
        async loginRequest(){
                axios
                    .post('http://localhost:5000/api/login',
                        {
                            emailFromRequest: this.frontend_email,
                            passwordFromRequest: this.frontend_password
                        }
                    )
                    .then((response) => {
                        console.log("good response",response)
                        this.frontend_message = response.data
                        if(response.status == 201){
                            localStorage.setItem('authToken', response.data.authToken)
                            localStorage.setItem('role', response.data.role)
                            this.$router.push({name: 'homeRoute'})
                        }
                    })
                    .catch((error) => {
                        console.log("bad response",error)
                    })
        },
    }
};
</script>