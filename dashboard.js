const $=selector=>document.querySelector(selector);

document.querySelectorAll('.tab').forEach(tab=>tab.onclick=()=>{
  document.querySelectorAll('.tab').forEach(item=>item.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(panel=>panel.classList.remove('active'));
  tab.classList.add('active');
  $('#'+tab.dataset.target).classList.add('active');
});

async function api(url,options={}){
  const response=await fetch(url,options),data=await response.json();
  if(!response.ok)throw Error(data.detail||'Request failed');
  return data;
}

function esc(value){
  return String(value??'').replace(/[&<>"']/g,character=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[character]));
}

function show(data){
  $('#result').innerHTML='<div class="card"><h2>Recommendation</h2><p>'+esc(data.summary)+'</p><p><b>Total:</b> INR '+Number(data.total_estimated).toLocaleString('en-IN')+' / INR '+Number(data.budget).toLocaleString('en-IN')+'</p><div class="result-grid">'+data.recommendations.map(item=>'<div class="item"><b>'+esc(item.name)+'</b><p>'+esc(item.description)+'</p><p>INR '+Number(item.estimated_price).toLocaleString('en-IN')+' · '+esc(item.platform)+'</p><a target="_blank" rel="noopener noreferrer" href="'+esc(item.search_url)+'">Search platform</a></div>').join('')+'</div></div>';
}

async function submit(url,form,multipart=false){
  try{
    const options={method:'POST'};
    if(multipart){
      options.body=new FormData(form);
    }else{
      const data=Object.fromEntries(new FormData(form));
      data.budget=Number(data.budget);
      if(url.includes('home')){
        data.rooms=data.rooms.split(',').map(value=>value.trim()).filter(Boolean);
        data.items={};
        (data.items_raw||'').split(',').forEach(pair=>{
          const [key,value]=pair.split('=');
          if(key)data.items[key.trim()]=Number(value)||0;
        });
        delete data.items_raw;
      }else if(url.includes('party')){
        data.guests=Number(data.guests);
      }else if(url.includes('travel')){
        data.days=Number(data.days);
        data.travelers=Number(data.travelers);
      }else if(url.includes('meal')){
        data.people=Number(data.people);
        data.days=Number(data.days);
      }else if(url.includes('shopping')){
        data.items=data.items_raw.split(',').map(value=>value.trim()).filter(Boolean);
        delete data.items_raw;
      }
      options.headers={'Content-Type':'application/json'};
      options.body=JSON.stringify(data);
    }
    show(await api(url,options));
    load();
  }catch(error){
    $('#result').innerHTML='<div class="card"><b>Error:</b> '+esc(error.message)+'</div>';
  }
}

[
  ['homeForm','/generate-home',false],['partyForm','/generate-party',false],
  ['jewelryForm','/generate-jewelry',true],['travelForm','/generate-travel',false],
  ['mealForm','/generate-meal',false],['shoppingForm','/generate-shopping',false]
].forEach(([formId,url,multipart])=>{
  $('#'+formId).onsubmit=event=>{event.preventDefault();submit(url,event.target,multipart);};
});

$('#logout').onclick=async()=>{await api('/logout',{method:'POST'});location='/login';};

async function load(){
  try{
    const records=await api('/history');
    $('#history').innerHTML=records.length?records.map(record=>'<p><b>'+esc(record.planner)+'</b> - '+esc(record.summary)+' <button onclick="openRec(\''+esc(record.id)+'\')">View</button></p>').join(''):'No recommendations yet.';
  }catch(error){
    $('#history').textContent='Login required.';
  }
}

async function openRec(id){show(await api('/recommendations-details/'+encodeURIComponent(id)));}
load();