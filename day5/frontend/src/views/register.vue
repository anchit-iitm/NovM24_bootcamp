<template>
    <div class="registration_page">
        <h2>registration page</h2>
        <form>
            <label for="emailid">email: </label>
            <input type="email" name="emailid" id="" placeholder="add the email" v-model="this.frontend_email"><br><br>
            <label for="passwrrd">passwrrd: </label>
            <input type="password" name="passwrrd" id="write the password" v-model="this.frontend_password"><br><br>
            <label for="role">role: </label>
            <select name="role" id="" v-model="this.frontend_role">
                <option value="manager">Manager</option>
                <option value="customer">Customer</option>
            </select><br><br>
            <button type="button" @click="this.registerRequest()">register</button>
        </form>
        {{ this.frontend_message }}
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: "registeration",
    data() {
        return {
            frontend_message: "",
            frontend_email: "",
            frontend_password: "",
            frontend_role: "",
        };
    },
    methods:{
        test(){
            console.log("email", this.frontend_email)
            console.log("passwrod", this.frontend_password)
            console.log("role", this.frontend_role)
        },
        async registerRequest(){
                axios
                    .post('http://localhost:5000/api/register',
                        {
                            emailFromRequest: this.frontend_email,
                            passwordFromRequest: this.frontend_password,
                            roleFromRequest: this.frontend_role
                        }
                    )
                    .then((response) => {
                        console.log("good response",response)
                        this.frontend_message = response.data
                    })
                    .catch((error) => {
                        console.log("bad response",error)
                    })
        },
    }
};
</script>