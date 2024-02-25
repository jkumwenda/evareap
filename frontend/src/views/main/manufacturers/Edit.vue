<template>
  <div class="flex flex-col space-y-4 flex-1">
    <HeaderView :headerTitle="headerTitle"></HeaderView>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
      <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editManufacturer" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Manufacturer
          </span>
          <input type="input" name="manufacturer" v-model="manufacturerData.manufacturer"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Manufacturer" />
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Address
          </span>
          <textarea name="address" v-model="manufacturerData.address"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Address"></textarea>
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Country
          </span>
          <select name="country"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            v-model="manufacturerData.country_id">
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
          <input type="email" name="email" v-model="manufacturerData.email"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="you@example.com" />
        </label>
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Phone
          </span>
          <input type="text" name="phone" v-model="manufacturerData.phone"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            title="Please enter a valid 10-digit phone number" placeholder="Phone number" required />
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Edit manufacturer
          </button>
          <router-link :to="{ name: 'Manufacturers' }"
            class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import { fetchData, updateItem, fetchItem } from "@/services/apiService";
import HeaderView from '@/includes/Header.vue'
import SpinnerComponent from "@/components/Spinner.vue";
import router from "@/router";

export default {
  name: "EditManufacturerView",
  components: {
    HeaderView, SpinnerComponent
  },
  data() {
    return {
      headerTitle: "Edit manufacturer",
      id: this.$route.params.id,
      manufacturerData: {
        manufacturer: "",
        address: "",
        country_id: "",
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
    this.getManufacturer();
    this.getCountries();
  },
  methods: {
    async editManufacturer() {
      this.isLoading = true;
      try {
        const response = await updateItem(
          "manufacturers",
          this.id,
          this.manufacturerData
        );
        this.manufacturer = response.data;
        this.isLoading = false;
        router.push("/manufacturers");
      } catch (error) {
        console.error("Error fetching manufacturer entities:", error);
        this.isLoading = false;
      }
    },
    async getManufacturer() {
      try {
        const response = await fetchItem("manufacturers", this.id);
        console.log(response)
        this.manufacturerData.manufacturer = response.manufacturer.manufacturer;
        this.manufacturerData.address = response.manufacturer.address;
        this.manufacturerData.country_id = response.manufacturer.country_id;
        this.manufacturerData.email = response.manufacturer.email;
        this.manufacturerData.phone = response.manufacturer.phone;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching manufacturer:", error);
        this.isLoading = false;
      }
    },
    async getCountries() {
      try {
        const response = await fetchData("countries/", this.currentPage, this.pageSize, this.searchPhrase);
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
