<template>
    <div class="createCategory">
        <h1>Add a new category</h1>
        <form @submit.prevent="this.addCategory()">
            <label for="name">name: </label>
                <input type="text" name="name" id="" v-model="this.name" required>
            <label for="description">description: </label>
                <input type="text" name="description" id="" v-model="this.description" required>
            <button type="submit">Add</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'categoryCreate',
    data() {
        return {
            name: '',
            description: '',
            token: ''
        }
    },
    beforeCreate() {
        // this.token = localStorage.getItem('authToken');
        if (!localStorage.getItem('authToken')) {
            this.$router.push({name: 'loginRoute'});
        }
        if (this.token && localStorage.getItem('role') !== 'admin') {
            this.$router.push({name: 'homeRoute'});
        }
    },
    created() {
        this.token = localStorage.getItem('authToken');
    },
    methods: {
        addCategory() {
           axios
                .post('http://localhost:5000/api/category', {
                    name: this.name,
                    description: this.description
                }, {
                    headers: {
                        'Authorization': `${this.token}`
                    }
                })
                .then((response) => {
                    if (response.status === 201) {
                        alert('Category added successfully');
                        this.$router.push({name: 'homeRoute'});
                    }
                })
                .catch((error) => {
                    alert('Failed to add category');
                });
        }
    }
}
</script>