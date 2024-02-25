<template>
  <div class="flex flex-col space-y-4 flex-1">
    <HeaderView :headerTitle="headerTitle"></HeaderView>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
      <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editAdministrationRoute" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Administration Route
          </span>
          <input type="input" name="administration_route" v-model="administrationRouteData.administration_route"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Administration route" />
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Description
          </span>
          <textarea name="description" v-model="administrationRouteData.description"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Description" required></textarea>
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Edit administration route
          </button>
          <router-link :to="{ name: 'AdministrationRoutes' }"
            class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import { updateItem, fetchItem } from "@/services/apiService";
import HeaderView from '@/includes/Header.vue'
import SpinnerComponent from "@/components/Spinner.vue";
import router from "@/router";

export default {
  name: "EditAdministrationRouteView",
  components: {
    HeaderView, SpinnerComponent
  },
  data() {
    return {
      headerTitle: "Edit administration route",
      id: this.$route.params.id,
      administrationRouteData: {
        administration_route: "",
        description: "",
      },
      isLoading: false,
      administration_route: {},
    };
  },
  mounted() {
    this.getAdministrationRoute();
  },
  methods: {
    async editAdministrationRoute() {
      this.isLoading = true;
      try {
        const response = await updateItem(
          "administration_routes",
          this.id,
          this.administrationRouteData
        );
        this.administration_route = response.data;
        this.isLoading = false;
        router.push("/administration-routes");
      } catch (error) {
        console.error("Error editing administration route:", error);
        this.isLoading = false;
      }
    },
    async getAdministrationRoute() {
      try {
        const response = await fetchItem("administration_routes", this.id);
        console.log(response)
        this.administrationRouteData.administration_route = response.administration_route;
        this.administrationRouteData.category_code = response.administration_route;
        this.administrationRouteData.description = response.administration_route;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching administration route:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
