<template>
    <!--BottomBar ist überall gleich, deswegen hart geschrieben ohne slots-->
    <div class="bottom-bar">
    <div class="left">
      <button class="bottom-btn" @click="$router.push('/listen')">
        📋 <span>Listen</span>
      </button>
    </div>

    <div class="middle">
      <button class="bottom-btn" @click="$router.push('/archiv')">
        📁 <span>Archiv</span>
      </button>

      <button class="bottom-btn" @click="$router.push('/fav')">
        ⭐ <span>Favoriten</span>
      </button>
    </div>

    <div class="right">
      <button class="bottom-btn" @click="$router.push('/settings')">
        ⚙️ <span>Einstellungen</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "BottomBar"
};
</script>