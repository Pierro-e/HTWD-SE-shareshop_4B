<template>
    <!--BottomBar ist überall gleich, deswegen hart geschrieben ohne slots-->
    <div class="bottom-bar">
      <button class="bottom-btn" @click="$router.push('/listen')">
        <div class=icon>
          <font-awesome-icon icon='list'/>
        </div>
        <span>Listen</span>
      </button>
    
      <button class="bottom-btn" @click="$router.push('/userArchive')">
        <div class=icon>
          <font-awesome-icon icon='box-archive'/>
        </div> 
        <span>Archiv</span>
      </button>

      <button class="bottom-btn" @click="$router.push('/fav')">
        <div class=icon>
          <font-awesome-icon icon='star'/>
        </div> 
        <span>Favoriten</span>
      </button>
   
      <button class="bottom-btn" @click="$router.push('/settings')">
        <div class=icon>
          <font-awesome-icon icon='gear'/> 
        </div>
        <span>Einstellungen</span>
      </button>
    
  </div>
</template>

<script>
export default {
  name: "BottomBar"
};
</script>

<style scoped>
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;

  background-color: var(--box-bg-color);
  box-shadow: 0 0px 5px 2px var(--box-shadow-color);

  font-size: x-small;

  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;

  z-index: 999;
}

.bottom-btn {
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;
  color: var(--text-color);
  background: none;
  border: none;
}

.bottom-btn .icon {
  font-size: large; 
  margin-bottom: 4px;
}
</style>