<template>
    <div>
      <h1>Welcome to the Dashboard</h1>
      <button @click="logout">Logout</button>
      <p>You are logged in!</p>
  
      <!-- Task Form to Create Task -->
      <h2>Create Task</h2>
      <form @submit.prevent="createTask">
        <input v-model="newTask.title" type="text" placeholder="Task Title" required />
        <textarea v-model="newTask.description" placeholder="Task Description" required></textarea>
        <input v-model="newTask.effort" type="number" placeholder="Effort (in Days)" required />
        <input v-model="newTask.dueDate" type="date" required />
        <button type="submit">Create Task</button>
      </form>
  
      <!-- Task List to View Tasks -->
      <h2>Your Tasks</h2>
      <ul>
        <li v-for="task in tasks" :key="task.id">
          <strong>{{ task.title }}</strong> - {{ task.dueDate }}
          <button @click="deleteTask(task.id)">Delete</button>
          <button @click="editTask(task)">Edit</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        newTask: {
          title: '',
          description: '',
          effort: 0,
          dueDate: ''
        },
        tasks: []
      };
    },
    methods: {
      logout() {
        localStorage.removeItem('token');
        this.$router.push('/login');
      },
      async fetchTasks() {
        const token = localStorage.getItem('token');
        const res = await fetch('http://localhost:8000/api/tasks/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const data = await res.json();
        this.tasks = data;
      },
  
      async createTask() {
        const token = localStorage.getItem('token');
        const res = await fetch('http://localhost:8000/api/tasks/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(this.newTask)
        });
  
        const data = await res.json();
        if (res.ok) {
          this.tasks.push(data);
          this.newTask = { title: '', description: '', effort: 0, dueDate: '' }; // Reset form
        } else {
          alert('Error creating task');
        }
      },
  
      async deleteTask(taskId) {
        const token = localStorage.getItem('token');
        const res = await fetch(`http://localhost:8000/api/tasks/${taskId}/`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
  
        if (res.ok) {
          this.tasks = this.tasks.filter(task => task.id !== taskId);
        } else {
          alert('Error deleting task');
        }
      },
  
      async updateTask() {
        const token = localStorage.getItem('token');
        const res = await fetch(`http://localhost:8000/api/tasks/${this.taskToEdit.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(this.taskToEdit)
        });
  
        const data = await res.json();
        if (res.ok) {
          this.fetchTasks(); // Refresh task list
          this.taskToEdit = null; // Clear editing state
        } else {
          alert('Error updating task');
        }
      },
  
      editTask(task) {
        this.taskToEdit = { ...task }; // Prepare task for editing
      }
    },
    created() {
      this.fetchTasks();
    }
  };
  </script>
  
  <style scoped>
  button {
    padding: 8px 12px;
    margin: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  form {
    margin-top: 20px;
  }
  
  input, textarea {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  h1 {
    font-size: 2em;
    margin-bottom: 20px;
  }
  
  h2 {
    font-size: 1.5em;
    margin-bottom: 10px;
  }
  </style>
  