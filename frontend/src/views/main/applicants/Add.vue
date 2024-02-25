<template>
  <div class="flex flex-col space-y-4 flex-1">
    <HeaderView :headerTitle="headerTitle"></HeaderView>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
      <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="addApplicant" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Applicant
          </span>
          <input type="input" name="applicant" v-model="applicantData.applicant"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Applicant" />
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Address
          </span>
          <textarea name="address" v-model="applicantData.address"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Address"></textarea>
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Country
          </span>
          <select name="country"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            v-model="applicantData.country_id">
            <option value="" disabled selected>--Select country--</option>
            <option v-for="country in countries" :key="country.id" :value="country.id">
              {{ country.country }}
            </option>
          </select>
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Email address
          </span>
          <input type="email" name="email" v-model="applicantData.email"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="you@example.com" />
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Phone
          </span>
          <input type="text" name="phone" v-model="applicantData.phone"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            title="Please enter a valid 10-digit phone number" placeholder="Phone number" required />
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Add applicant
          </button>
          <router-link :to="{ name: 'Applicants' }"
            class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import { createItem, fetchData } from "@/services/apiService";
import HeaderView from '@/includes/Header.vue'
import SpinnerComponent from "@/components/Spinner.vue";
import router from "@/router";

export default {
  name: "AddApplicantView",
  components: {
    HeaderView, SpinnerComponent
  },
  data() {
    return {
      headerTitle: "Add applicant",
      applicantData: {
        applicant: "",
        address: "",
        country: "",
        email: "",
        phone: "",
      },
      isLoading: false,
      countries: {},
      currentPage: 1,
      totalPages: "",
      pageSize: 500,
      searchPhrase: ""
    };
  },
  mounted() {
    this.getCountries();
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
    async getCountries() {
      try {
        const response = await fetchData("countries", this.currentPage, this.pageSize, this.searchPhrase);
        this.countries = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching countries:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
