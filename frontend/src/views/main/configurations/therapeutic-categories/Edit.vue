<template>
  <div class="flex flex-col space-y-4 flex-1">
    <HeaderView :headerTitle="headerTitle"></HeaderView>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
      <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editTherapeuticCategory" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Therapeutic Category
          </span>
          <input type="input" name="therapeutic_category" v-model="therapeuticCategoryData.therapeutic_category"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Therapeutic category" />
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Description
          </span>
          <textarea name="description" v-model="therapeuticCategoryData.description"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Description" required></textarea>
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Edit therapeutic category
          </button>
          <router-link :to="{ name: 'TherapeuticCategories' }"
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
  name: "EditTherapeuticCategoryView",
  components: {
    HeaderView, SpinnerComponent
  },
  data() {
    return {
      headerTitle: "Edit therapeutic category",
      id: this.$route.params.id,
      therapeuticCategoryData: {
        therapeutic_category: "",
        category_code: "",
        description: "",
      },
      isLoading: false,
      therapeutic_category: {},
    };
  },
  mounted() {
    this.getTherapeuticCategory();
  },
  methods: {
    async editTherapeuticCategory() {
      this.isLoading = true;
      try {
        const response = await updateItem(
          "therapeutic_categories",
          this.id,
          this.therapeuticCategoryData
        );
        this.therapeutic_category = response.data;
        this.isLoading = false;
        router.push("/therapeutic-categories");
      } catch (error) {
        console.error("Error editing therapeutic category:", error);
        this.isLoading = false;
      }
    },
    async getTherapeuticCategory() {
      try {
        const response = await fetchItem("therapeutic_categories", this.id);
        console.log(response)
        this.therapeuticCategoryData.therapeutic_category = response.therapeutic_category;
        this.therapeuticCategoryData.description = response.description;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching therapeutic category:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
