<template>
  <div class="flex flex-col space-y-4 flex-1">
    <HeaderView :headerTitle="headerTitle"></HeaderView>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
      <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editGenericName" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Generic Name
          </span>
          <input type="input" name="generic_name" v-model="genericNameData.generic_name"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Generic name" />
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Description
          </span>
          <textarea name="description" v-model="genericNameData.description"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Description" required></textarea>
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Edit generic name
          </button>
          <router-link :to="{ name: 'GenericNames' }"
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
  name: "EditGenericNameView",
  components: {
    HeaderView, SpinnerComponent
  },
  data() {
    return {
      headerTitle: "Edit generic name",
      id: this.$route.params.id,
      genericNameData: {
        generic_name: "",
        description: "",
      },
      isLoading: false,
      generic_name: {},
    };
  },
  mounted() {
    this.getGenericName();
  },
  methods: {
    async editGenericName() {
      this.isLoading = true;
      try {
        const response = await updateItem(
          "generic_names",
          this.id,
          this.genericNameData
        );
        this.generic_name = response.data;
        this.isLoading = false;
        router.push("/generic-names");
      } catch (error) {
        console.error("Error editing generic name:", error);
        this.isLoading = false;
      }
    },
    async getGenericName() {
      try {
        const response = await fetchItem("generic_names", this.id);
        console.log(response)
        this.genericNameData.generic_name = response.generic_name;
        this.genericNameData.description = response.description;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching generic name:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
