<template>
    <div>
      <h1>Manage Tasks</h1>
      <ul>
        <li v-for="task in tasks" :key="task.id">
          <strong>{{ task.title }}</strong> - {{ task.due_date }}
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
        tasks: []
      };
    },
    methods: {
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
  
      editTask(task) {
        this.$router.push({ name: 'edit-task', params: { taskId: task.id } });
      }
    },
    created() {
      this.fetchTasks();
    }
  };
  </script>
  