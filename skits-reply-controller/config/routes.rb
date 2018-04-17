Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  post 'addSkitReply', action: :addSkitReply, controller: 'skit'
  post 'removeSkitReply', action: :removeSkitReply, controller: 'skit'
  get 'getSkitReplies', action: :getSkitReplies, controller: 'skit'
end
