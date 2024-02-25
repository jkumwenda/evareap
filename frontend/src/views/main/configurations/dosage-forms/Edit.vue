<template>
  <div class="flex flex-col space-y-4 flex-1">
    <HeaderView :headerTitle="headerTitle"></HeaderView>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
      <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editDosageForm" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Dosage Form
          </span>
          <input type="input" name="dosage_form" v-model="dosageFormData.dosage_form"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Dosage form" />
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Description
          </span>
          <textarea name="description" v-model="dosageFormData.description"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Description" required></textarea>
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Edit dosage form
          </button>
          <router-link :to="{ name: 'DosageForms' }"
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
  name: "EditDosageFormView",
  components: {
    HeaderView, SpinnerComponent
  },
  data() {
    return {
      headerTitle: "Edit dosage form",
      id: this.$route.params.id,
      dosageFormData: {
        dosage_form: "",
        description: "",
      },
      isLoading: false,
      dosage_form: {},
    };
  },
  mounted() {
    this.getDosageForm();
  },
  methods: {
    async editDosageForm() {
      this.isLoading = true;
      try {
        const response = await updateItem(
          "dosage_forms",
          this.id,
          this.dosageFormData
        );
        this.dosage_form = response.data;
        this.isLoading = false;
        router.push("/dosage-forms");
      } catch (error) {
        console.error("Error editing dosage form:", error);
        this.isLoading = false;
      }
    },
    async getDosageForm() {
      try {
        const response = await fetchItem("dosage_forms", this.id);
        this.dosageFormData.dosage_form = response.dosage_form;
        this.dosageFormData.description = response.description;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching dosage form:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
