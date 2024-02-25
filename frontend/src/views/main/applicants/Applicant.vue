<template>
  <div class="flex flex-col space-y-4 flex-1">
    <HeaderView :headerTitle="headerTitle"></HeaderView>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
      Applicant details goes here
    </div>
  </div>
</template>
<script>
import { createItem } from "@/services/apiService";
import HeaderView from '@/includes/Header.vue'
import SpinnerComponent from "@/components/Spinner.vue";
import router from "@/router";

export default {
  name: "ApplicantView",
  components: {
    HeaderView, SpinnerComponent
  },
  data() {
    return {
      headerTitle: "Applicant details",
      applicantData: {
        firstname: "",
        lastname: "",
        email: "",
        phone: "",
        password: "password",
      },
      isLoading: false,
    };
  },
  methods: {
    async addApplicant() {
      this.isLoading = true;
      try {
        const response = await createItem("applicants/", this.applicantData);
        this.applicants = response.data;
        this.isLoading = false;
        router.push("/applicants");
      } catch (error) {
        console.error("Error fetching applicants:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
