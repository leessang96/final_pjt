<template>

  <!-- 네비게이션 -->
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">Navbar</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <RouterLink :to="{ name: 'comparisonDeposit'}" class="nav-link">예금비교</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'cashProduct'}" class="nav-link">현물상품</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'bankMap'}" class="nav-link">은행지도</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'articles'}" class="nav-link">게시판</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'logIn'}" class="nav-link">로그인</RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <main>
    <div class="container">
      <RouterView/>
    </div>
  </main>
</template>

<script setup>
  import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>

</style>