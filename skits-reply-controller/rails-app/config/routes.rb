Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  post 'addSkitReply', action: :addSkitReply, controller: 'skits'
  post 'removeSkitReply', action: :removeSkitReply, controller: 'skits'
  get 'getSkitReplies', action: :getSkitReplies, controller: 'skits'
end
